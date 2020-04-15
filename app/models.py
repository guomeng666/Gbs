from . import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


# 角色表
class Role(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True)  # 角色编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    createTime = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    updateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    users = db.relationship('User', backref='role', foreign_keys="User.roleId")


# 部门表
class DepartMent(db.Model):
    __tablename__ = "DepartMents"
    id = db.Column(db.Integer, primary_key=True)  # 部门编号
    name = db.Column(db.String(100), unique=True)  # 部门名称
    createTime = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    updateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    users = db.relationship('User', backref='departMent', foreign_keys="User.departMentId")


# 用户-角色表
class UserRole:
    __tablename__ = "UserRoles"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    userId = db.Column(db.String(100), db.ForeignKey('Users.id'))  # 部门名称
    roleId = db.Column(db.String(100), db.ForeignKey('Roles.id'))  # 部门名称


# 用户表
class User(db.Model):
    __tablename__ = "Users"  # 必须和类型相同,而且是小写,要不第二次生成迁移脚本然后更新数据库会出错
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(100), unique=True)  # 用户名字
    passwordHash = db.Column(db.String(100))  # 用户密码
    identityId = db.Column(db.String(100))  # 身份证号码
    address = db.Column(db.String(200))  # 身份证住址
    departMentId = db.Column(db.Integer, db.ForeignKey('DepartMents.id'))  # 部门ID
    lastLoginTime = db.Column(db.DateTime, default=datetime.now)  # 最后登录时间
    createTime = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    updateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    roles = db.relationship("Role", secondary=UserRole, backref=db.backref("users", lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return "<Admin %r>" % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        """
        检测密码是否正确
        :param password: 密码
        :return: 返回布尔值
        """
        return check_password_hash(self.password_hash, password)

    def updated_logon_time(self):
        self.lastLoginTime = datetime.now()

