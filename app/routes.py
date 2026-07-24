from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from sqlalchemy import or_
from datetime import datetime
from app.models import User, ServiceTicket, Asset, db


def register_routes(app):
    # ==========================================
    # Helper Functions
    # ==========================================

    def is_employee():
        return (
            "user_id" in session and
            session["role"] == "Employee"
        )

    def is_it_staff():
        return (
            "user_id" in session and
            session["role"] == "IT Staff"
        )

    def is_manager():
        return (
            "user_id" in session and
            session["role"] == "IT Manager"
        )

    # -----------------------------
    # Login
    # -----------------------------
    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":

            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(
                username=username,
                password=password
            ).first()

            if user:

                session["user_id"] = user.id
                session["full_name"] = user.full_name
                session["username"] = user.username
                session["role"] = user.role
                session["department"] = user.department

                if user.role == "Employee":
                    return redirect(url_for("employee_dashboard"))

                elif user.role == "IT Staff":
                    return redirect(url_for("it_dashboard"))

                elif user.role == "IT Manager":
                    return redirect(url_for("manager_dashboard"))

            return "Invalid Username or Password"

        return render_template("login.html")

    # -----------------------------
    # Logout
    # -----------------------------
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    # -----------------------------
    # Employee Dashboard
    # -----------------------------
    @app.route("/employee")
    def employee_dashboard():

        if not is_employee():
            return redirect(url_for("home"))

        total = ServiceTicket.query.filter_by(
            employee_name=session["full_name"]
        ).count()

        open_count = ServiceTicket.query.filter_by(
            employee_name=session["full_name"],
            status="Open"
        ).count()

        progress = ServiceTicket.query.filter_by(
            employee_name=session["full_name"],
            status="In Progress"
        ).count()

        resolved = ServiceTicket.query.filter_by(
            employee_name=session["full_name"],
            status="Resolved"
        ).count()

        closed = ServiceTicket.query.filter_by(
            employee_name=session["full_name"],
            status="Closed"
        ).count()

        recent = ServiceTicket.query.filter_by(
            employee_name=session["full_name"]
        ).order_by(
            ServiceTicket.created_at.desc()
        ).limit(5).all()

        return render_template(
            "employee_dashboard.html",
            name=session["full_name"],
            total=total,
            open=open_count,
            progress=progress,
            resolved=resolved,
            closed=closed,
            recent=recent
        )

    # -----------------------------
    # Create Ticket
    # -----------------------------
    @app.route("/employee/create-ticket", methods=["GET", "POST"])
    def create_ticket():

        if not is_employee():
            return redirect(url_for("home"))

        if request.method == "POST":

            ticket = ServiceTicket(
                ticket_number=f"NHPC-{ServiceTicket.query.count()+1:05}",
                employee_name=session["full_name"],
                department=request.form["department"],
                category=request.form["category"],
                priority=request.form["priority"],
                problem=request.form["problem"]
            )

            db.session.add(ticket)
            db.session.commit()

            return redirect(url_for("my_complaints"))

        return render_template("create_ticket.html")

    # -----------------------------
    # My Complaints
    # -----------------------------
    @app.route("/employee/my-complaints")
    def my_complaints():

        if not is_employee():
            return redirect(url_for("home"))

        tickets = ServiceTicket.query.filter_by(
            employee_name=session["full_name"]
        ).order_by(
            ServiceTicket.created_at.desc()
        ).all()

        return render_template(
            "my_complaints.html",
            tickets=tickets
        )

    # -----------------------------
    # IT Dashboard
    # -----------------------------
    @app.route("/it")
    def it_dashboard():

        if not is_it_staff():
            return redirect(url_for("home"))

        total = ServiceTicket.query.count()

        open_count = ServiceTicket.query.filter_by(
            status="Open"
        ).count()

        progress = ServiceTicket.query.filter_by(
            status="In Progress"
        ).count()

        resolved = ServiceTicket.query.filter_by(
            status="Resolved"
        ).count()

        closed = ServiceTicket.query.filter_by(
            status="Closed"
        ).count()

        recent = ServiceTicket.query.order_by(
            ServiceTicket.created_at.desc()
        ).limit(5).all()

        return render_template(
            "it_dashboard.html",
            total=total,
            open=open_count,
            progress=progress,
            resolved=resolved,
            closed=closed,
            recent=recent
        )

    # -----------------------------
    # View All Tickets
    # -----------------------------
    @app.route("/it/all-tickets")
    def all_tickets():

        if not is_it_staff():
            return redirect(url_for("home"))

        tickets = ServiceTicket.query.order_by(
            ServiceTicket.created_at.desc()
        ).all()

        return render_template(
            "all_tickets.html",
            tickets=tickets
        )

    # -----------------------------
    # Ticket Details
    # -----------------------------
    @app.route("/it/ticket/<int:ticket_id>", methods=["GET", "POST"])
    def ticket_details(ticket_id):

        if not (is_it_staff() or is_manager()):
            return redirect(url_for("home"))

        ticket = ServiceTicket.query.get_or_404(ticket_id)

        if request.method == "POST":

            ticket.status = request.form["status"]
            ticket.assigned_to = request.form["assigned_to"]
            ticket.resolution_notes = request.form["resolution_notes"]
            ticket.updated_by = session["full_name"]

            if ticket.status == "Closed":
                ticket.closed_at = datetime.utcnow()

            db.session.commit()

            if is_manager():
                return redirect(url_for("manager_tickets"))
            else:
                return redirect(url_for("all_tickets"))

        return render_template(
            "ticket_details.html",
            ticket=ticket
        )

    # -----------------------------
    # Manager Dashboard
    # -----------------------------
    @app.route("/manager")
    def manager_dashboard():

        if "user_id" not in session or session["role"] != "IT Manager":
            return redirect(url_for("home"))

        total = ServiceTicket.query.count()

        open_count = ServiceTicket.query.filter_by(
            status="Open"
        ).count()

        progress = ServiceTicket.query.filter_by(
            status="In Progress"
        ).count()

        resolved = ServiceTicket.query.filter_by(
            status="Resolved"
        ).count()

        closed = ServiceTicket.query.filter_by(
            status="Closed"
        ).count()

        total_users = User.query.count()

        active_users = User.query.filter_by(
            status="Active"
        ).count()

        total_assets = Asset.query.count()

        return render_template(
            "manager_dashboard.html",
            total=total,
            open=open_count,
            progress=progress,
            resolved=resolved,
            closed=closed,
            total_users=total_users,
            active_users=active_users,
            total_assets=total_assets
        )

    # -----------------------------
    # Manage Users
    # -----------------------------
    @app.route("/manager/users")
    def manage_users():

        if not is_manager():
            return redirect(url_for("home"))

        search = request.args.get("search", "")

        if search:

            users = User.query.filter(

                or_(

                    User.full_name.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                    User.department.ilike(f"%{search}%"),
                    User.role.ilike(f"%{search}%")

                )

            ).order_by(
                User.full_name
            ).all()

        else:

            users = User.query.order_by(
                User.full_name
            ).all()

        return render_template(
            "manage_users.html",
            users=users,
            search=search
        )

    # -----------------------------
    # Manage Tickets
    # -----------------------------
    @app.route("/manager/tickets")
    def manager_tickets():

        if not is_manager():
            return redirect(url_for("home"))

        search = request.args.get("search", "")

        if search:

            tickets = ServiceTicket.query.filter(

                or_(

                    ServiceTicket.ticket_number.ilike(f"%{search}%"),
                    ServiceTicket.employee_name.ilike(f"%{search}%"),
                    ServiceTicket.department.ilike(f"%{search}%"),
                    ServiceTicket.status.ilike(f"%{search}%")

                )

            ).order_by(
                ServiceTicket.created_at.desc()
            ).all()

        else:

            tickets = ServiceTicket.query.order_by(
                ServiceTicket.created_at.desc()
            ).all()

        return render_template(
            "all_tickets.html",
            tickets=tickets,
            search=search
        )
    
    # =====================================================
    # Add User
    # =====================================================

    @app.route("/manager/add-user", methods=["GET", "POST"])
    def add_user():
        if not is_manager():
            return redirect(url_for("home"))

        if request.method == "POST":

            # Check if username already exists
            existing = User.query.filter_by(
              username=request.form["username"]
            ).first()

            if existing:
                flash("Username already exists.", "danger")
                return redirect(url_for("add_user"))

            user = User(

               full_name=request.form["full_name"],
               username=request.form["username"],
               password=request.form["password"],
               role=request.form["role"],
               department=request.form["department"],
               email=request.form["email"],
               status="Active"

           )

            db.session.add(user)
            db.session.commit()

            flash("User created successfully.", "success")

            return redirect(url_for("manage_users"))

        return render_template("add_user.html")
    # =====================================================
    # Edit User
    # =====================================================

    @app.route("/manager/edit-user/<int:user_id>", methods=["GET", "POST"])
    def edit_user(user_id):

       if not is_manager():
            return redirect(url_for("home"))

       user = User.query.get_or_404(user_id)

       if request.method == "POST":

            user.full_name = request.form["full_name"]
            user.username = request.form["username"]
            user.password = request.form["password"]
            user.role = request.form["role"]
            user.department = request.form["department"]
            user.email = request.form["email"]
            user.status = request.form["status"]

            db.session.commit()

            flash("User updated successfully.", "success")

            return redirect(url_for("manage_users"))

       return render_template(
            "edit_user.html",
            user=user
       )
    

    # =====================================================
    # Delete User
    # =====================================================

    @app.route("/manager/delete-user/<int:user_id>")
    def delete_user(user_id):

       if not is_manager():
           return redirect(url_for("home"))

       user = User.query.get_or_404(user_id)

       # Prevent deleting yourself
       if user.id == session["user_id"]:
           flash("You cannot delete your own account.", "danger")
           return redirect(url_for("manage_users"))

       db.session.delete(user)
       db.session.commit()

       flash("User deleted successfully.", "success")

       return redirect(url_for("manage_users"))
    
    # -----------------------------
    # Manage Assets
    # -----------------------------
    @app.route("/manager/assets")
    def manage_assets():

        if not is_manager():
            return redirect(url_for("home"))

        search = request.args.get("search", "")

        if search:

            assets = Asset.query.filter(

                or_(

                    Asset.asset_code.ilike(f"%{search}%"),
                    Asset.asset_name.ilike(f"%{search}%"),
                    Asset.brand.ilike(f"%{search}%"),
                    Asset.location.ilike(f"%{search}%")

                )

            ).order_by(
                Asset.asset_name
            ).all()

        else:

            assets = Asset.query.order_by(
                Asset.asset_name
            ).all()

        return render_template(
            "manage_assets.html",
            assets=assets,
            search=search
        )
    
    # =====================================================
    # Import Assets From Excel
    # =====================================================

    @app.route("/manager/import-assets")
    def import_assets():

        if not is_manager():
           return redirect(url_for("home"))

        import pandas as pd

        path = "excel/Asseta_list.xlsx"

        df = pd.read_excel(path)

        imported = 0

        for _, row in df.iterrows():

           asset_code = str(row["Object"]).strip()

           if Asset.query.filter_by(asset_code=asset_code).first():
               continue

           asset = Asset(

               asset_code=asset_code,

               asset_name=str(row["Object Description"]),

               category=str(row["Object Physical Location"]),

               brand=str(row["Supplier Name"]),

               model="",

               serial_number="",

               location=str(row["Site Description"]),

               assigned_to=str(row["Object Custodian"]),

               status=str(row["Object Status"]),

               remarks=""

           )

           db.session.add(asset)

           imported += 1

        db.session.commit()

        flash(f"{imported} assets imported successfully.", "success")

        return redirect(url_for("manage_assets"))
    

    # =====================================================
    # Asset Details
    # =====================================================

    @app.route("/manager/asset/<int:asset_id>")
    def asset_details(asset_id):

         if not is_manager():
           return redirect(url_for("home"))

         asset = Asset.query.get_or_404(asset_id)

         return render_template(
           "asset_details.html",
           asset=asset
         )    
    

    # =====================================================
    # Edit Asset
    # =====================================================

    @app.route("/manager/asset/edit/<int:asset_id>", methods=["GET", "POST"])
    def edit_asset(asset_id):

        if not is_manager():
             return redirect(url_for("home"))

        asset = Asset.query.get_or_404(asset_id)

        if request.method == "POST":

             asset.assigned_to = request.form["assigned_to"]

             asset.location = request.form["location"]

             asset.status = request.form["status"]

             asset.remarks = request.form["remarks"]

             db.session.commit()

             flash("Asset updated successfully.", "success")

             return redirect(url_for("asset_details", asset_id=asset.id))

        return render_template(
             "edit_asset.html",
             asset=asset
        )
    

    # =====================================================
    # Delete Asset
    # =====================================================

    @app.route("/manager/asset/delete/<int:asset_id>")
    def delete_asset(asset_id):

        if not is_manager():
           return redirect(url_for("home"))

        asset = Asset.query.get_or_404(asset_id)

        db.session.delete(asset)

        db.session.commit()

        flash("Asset deleted successfully.")

        return redirect(url_for("manage_assets"))