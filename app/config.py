class Config:
    SECRET_KEY = "nhpc-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:YOUR_PASSWORD@localhost/complaint_system"

    SQLALCHEMY_TRACK_MODIFICATIONS = False