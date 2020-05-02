from . import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


# 部门表
class Department(db.Model):
    __tablename__ = "department"
    ID = db.Column(db.Integer, primary_key=True)  # 部门编号
    Name = db.Column(db.String(100), unique=True)  # 部门名称
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    Users = db.relationship('User', backref='Department')


# # 角色-权限表
# RolePrimissions = db.Table('roleprimissions',
#                      db.Column('RoleID', db.Integer, db.ForeignKey('role.ID')),
#                      db.Column('PrimissionID', db.Integer, db.ForeignKey('primission.ID')))


# 角色表
class Role(db.Model):
    __tablename__ = "role"
    ID = db.Column(db.Integer, primary_key=True)  # 角色编号
    Name = db.Column(db.String(100), unique=True)  # 角色名称
    PermissonID = db.Column(db.Integer, db.ForeignKey('primission.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    # Primissions = db.relationship("Primisson", secondary=RolePrimissions,
    #                               backref=db.backref("Roles", lazy='dynamic'), lazy='dynamic')


# 权限表
class Primisson(db.Model):
    __tablename__ = "primission"
    ID = db.Column(db.Integer, primary_key=True)  # 权限编号
    Name = db.Column(db.String(100), unique=True)  # 权限名称
    Quer = db.Column(db.Integer)  # 查询权限
    Maintain = db.Column(db.Integer)  # 维护权限
    Register = db.Column(db.Integer)  # 登记权限
    Sampling = db.Column(db.Integer)  # 扦样权限
    Assay = db.Column(db.Integer)  # 化验室权限
    Sell = db.Column(db.Integer)  # 售粮权限
    Weigh = db.Column(db.Integer)  # 检斤权限
    Unload = db.Column(db.Integer)  # 卸粮权限
    Settlement = db.Column(db.Integer)  # 结算权限
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    Roles = db.relationship('Role', backref='Permissons', foreign_keys="Role.PermissonID")


# 用户-角色表
UserRoles = db.Table('userroles',
                     db.Column('UserID', db.Integer, db.ForeignKey('user.ID')),
                     db.Column('RoleID', db.Integer, db.ForeignKey('role.ID')))


# 用户表
class User(db.Model):
    __tablename__ = "user"  # 必须和类型相同,而且是小写,要不第二次生成迁移脚本然后更新数据库会出错
    ID = db.Column(db.Integer, primary_key=True)  # 用户编号
    Name = db.Column(db.String(100), unique=True)  # 用户名字
    PasswordHash = db.Column(db.String(100))  # 用户密码
    IdentityID = db.Column(db.String(100))  # 身份证号码
    Address = db.Column(db.String(200))  # 身份证住址
    DepartmentID = db.Column(db.Integer, db.ForeignKey('department.ID'))  # 部门ID
    LastLoginTime = db.Column(db.DateTime)  # 最后登录时间
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    Roles = db.relationship("Role", secondary=UserRoles, backref=db.backref("Users", lazy='dynamic'), lazy='dynamic')

    VehicleTypeCreater = db.relationship('VehicleType', backref='Creater', foreign_keys="VehicleType.CreateID")
    VehicleTypeUpdater = db.relationship('VehicleType', backref='Updater', foreign_keys="VehicleType.UpdateID")

    BankTypeCreater = db.relationship('BankType', backref='Creater', foreign_keys="BankType.CreateID")
    BankTypeUpdater = db.relationship('BankType', backref='Updater', foreign_keys="BankType.UpdateID")

    ContractTypeCreater = db.relationship('ContractType', backref='Creater', foreign_keys="ContractType.CreateID")
    ContractTypeUpdater = db.relationship('ContractType', backref='Updater', foreign_keys="ContractType.UpdateID")

    PakeTypeCreater = db.relationship('PakeType', backref='Creater', foreign_keys="PakeType.CreateID")
    PakeTypeUpdater = db.relationship('PakeType', backref='Updater', foreign_keys="PakeType.UpdateID")

    PaymentTypeCreater = db.relationship('PaymentType', backref='Creater', foreign_keys="PaymentType.CreateID")
    PaymentTypeUpdater = db.relationship('PaymentType', backref='Updater', foreign_keys="PaymentType.UpdateID")

    SampleClassCreater = db.relationship('SampleClass', backref='Creater', foreign_keys="SampleClass.CreateID")
    SampleClassUpdater = db.relationship('SampleClass', backref='Updater', foreign_keys="SampleClass.UpdateID")

    CerealsTypeCreater = db.relationship('CerealsType', backref='Creater', foreign_keys="CerealsType.CreateID")
    CerealsTypeUpdater = db.relationship('CerealsType', backref='Updater', foreign_keys="CerealsType.UpdateID")

    TransprotCompanyCreater = db.relationship('TransprotCompany', backref='Creater',
                                              foreign_keys="TransprotCompany.CreateID")
    TransprotCompanyUpdater = db.relationship('TransprotCompany', backref='Updater',
                                              foreign_keys="TransprotCompany.UpdateID")

    SupplierCreater = db.relationship('Supplier', backref='Creater', foreign_keys="Supplier.CreateID")
    SupplierUpdater = db.relationship('Supplier', backref='Updater', foreign_keys="Supplier.UpdateID")

    ProcedureNodeCreater = db.relationship('ProcedureNode', backref='Creater', foreign_keys="ProcedureNode.CreateID")
    ProcedureNodeUpdater = db.relationship('ProcedureNode', backref='Updater', foreign_keys="ProcedureNode.UpdateID")

    PurchaseTypeCreater = db.relationship('PurchaseType', backref='Creater', foreign_keys="PurchaseType.CreateID")
    PurchaseTypeUpdater = db.relationship('PurchaseType', backref='Updater', foreign_keys="PurchaseType.UpdateID")

    WareHouseTypeCreater = db.relationship('WareHouseType', backref='Creater', foreign_keys="WareHouseType.CreateID")
    WareHouseTypeUpdater = db.relationship('WareHouseType', backref='Updater', foreign_keys="WareHouseType.UpdateID")

    PictureRegisterCreater = db.relationship('PictureRegister', backref='Creater',
                                             foreign_keys="PictureRegister.CreateID")
    PictureRegisterUpdater = db.relationship('PictureRegister', backref='Updater',
                                             foreign_keys="PictureRegister.UpdateID")

    PictureSampleCreater = db.relationship('PictureSample', backref='Creater', foreign_keys="PictureSample.CreateID")
    PictureSampleUpdater = db.relationship('PictureSample', backref='Updater', foreign_keys="PictureSample.UpdateID")

    PictureAssayCreater = db.relationship('PictureAssay', backref='Creater', foreign_keys="PictureAssay.CreateID")
    PictureAssayUpdater = db.relationship('PictureAssay', backref='Updater', foreign_keys="PictureAssay.UpdateID")

    PictureSellCreater = db.relationship('PictureSell', backref='Creater', foreign_keys="PictureSell.CreateID")
    PictureSellUpdater = db.relationship('PictureSell', backref='Updater', foreign_keys="PictureSell.UpdateID")

    PictureWeighCreater = db.relationship('PictureWeigh', backref='Creater', foreign_keys="PictureWeigh.CreateID")
    PictureWeighUpdater = db.relationship('PictureWeigh', backref='Updater', foreign_keys="PictureWeigh.UpdateID")

    PictureUnloadCreater = db.relationship('PictureUnload', backref='Creater', foreign_keys="PictureUnload.CreateID")
    PictureUnloadUpdater = db.relationship('PictureUnload', backref='Updater', foreign_keys="PictureUnload.UpdateID")

    PictureSettlementCreater = db.relationship('PictureSettlement', backref='Creater',
                                               foreign_keys="PictureSettlement.CreateID")
    PictureSettlementUpdater = db.relationship('PictureSettlement', backref='Updater',
                                               foreign_keys="PictureSettlement.UpdateID")

    SellerCreater = db.relationship('Seller', backref='Creater', foreign_keys="Seller.CreateID")
    SellerUpdater = db.relationship('Seller', backref='Updater', foreign_keys="Seller.UpdateID")

    VehicleCreater = db.relationship('Vehicle', backref='Creater', foreign_keys="Vehicle.CreateID")
    VehicleUpdater = db.relationship('Vehicle', backref='Updater', foreign_keys="Vehicle.UpdateID")

    ValuationCreater = db.relationship('Valuation', backref='Creater', foreign_keys="Valuation.CreateID")
    ValuationUpdater = db.relationship('Valuation', backref='Updater', foreign_keys="Valuation.UpdateID")

    ContractCreater = db.relationship('Contract', backref='Creater', foreign_keys="Contract.CreateID")
    ContractUpdater = db.relationship('Contract', backref='Updater', foreign_keys="Contract.UpdateID")

    RegisterCreater = db.relationship('Register', backref='Creater', foreign_keys="Register.CreateID")
    RegisterUpdater = db.relationship('Register', backref='Updater', foreign_keys="Register.UpdateID")

    SamplingCreater = db.relationship('Sampling', backref='Creater', foreign_keys="Sampling.CreateID")
    SamplingUpdater = db.relationship('Sampling', backref='Updater', foreign_keys="Sampling.UpdateID")

    AssayCreater = db.relationship('Assay', backref='Creater', foreign_keys="Assay.CreateID")
    AssayUpdater = db.relationship('Assay', backref='Updater', foreign_keys="Assay.UpdateID")

    SellCreater = db.relationship('Sell', backref='Creater', foreign_keys="Sell.CreateID")
    SellUpdater = db.relationship('Sell', backref='Updater', foreign_keys="Sell.UpdateID")

    WeighCreater = db.relationship('Weigh', backref='Creater', foreign_keys="Weigh.CreateID")
    WeighUpdater = db.relationship('Weigh', backref='Updater', foreign_keys="Weigh.UpdateID")

    UnloadCreater = db.relationship('Unload', backref='Creater', foreign_keys="Unload.CreateID")
    UnloadUpdater = db.relationship('Unload', backref='Updater', foreign_keys="Unload.UpdateID")

    SettlementCreater = db.relationship('Settlement', backref='Creater', foreign_keys="Settlement.CreateID")
    SettlementUpdater = db.relationship('Settlement', backref='Updater', foreign_keys="Settlement.UpdateID")

    Frozens = db.relationship('Procedure', backref='Frozener', foreign_keys="Procedure.FrozenerID")

    def __repr__(self):
        return "<Admin %r>" % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        """
        检测密码是否正确
        :param password: 密码
        :return: 返回布尔值
        """
        return check_password_hash(self.password_hash, password)

    def updated_logon_time(self):
        self.LastLoginTime = datetime.now()


# 车辆类型
class VehicleType(db.Model):
    __tablename__ = "vehicletype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    EstimateLoad = db.Column(db.Integer)  # 预估重量
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Vehicles = db.relationship('Vehicle', backref='VehicleType', foreign_keys="Vehicle.VehicleTypeID")


# 银行卡类型
class BankType(db.Model):
    __tablename__ = "banktype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Sellers = db.relationship('Seller', backref='BankType', foreign_keys="Seller.BankTypeID")
    Contracts = db.relationship('Contract', backref='BankType', foreign_keys="Contract.BankTypeID")


# 合同类型
class ContractType(db.Model):
    __tablename__ = "contracttype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='ContractType', foreign_keys="Contract.ContractTypeID")


# 粮食包装类型
class PakeType(db.Model):
    __tablename__ = "packtype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Registers = db.relationship('Register', backref='PackType')


# 支付方式
class PaymentType(db.Model):
    __tablename__ = "paymenttype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='PaymentType', foreign_keys="Contract.PaymentTypeID")
    Registers = db.relationship('Register', backref='PaymentType', foreign_keys="Register.PaymentTypeID")


# 样品级别
class SampleClass(db.Model):
    __tablename__ = "sampleclass"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Assays = db.relationship('Assay', backref='SampleClass')


# 粮食类型
class CerealsType(db.Model):
    __tablename__ = "cerealstype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 类型名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='CerealsType', foreign_keys="Contract.CerealsTypeID")
    Registers = db.relationship('Register', backref='CerealsType')
    Assays = db.relationship('Assay', backref='CerealsType')


# 运输公司
class TransprotCompany(db.Model):
    __tablename__ = "transportcompany"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 公司名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='TransprotCompany', foreign_keys="Contract.TransportCompanyID")


# 供应商
class Supplier(db.Model):
    __tablename__ = "supplier"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 供应商名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='Supplier', foreign_keys="Contract.SupplierID")


# 流程节点
class ProcedureNode(db.Model):
    __tablename__ = "procedurenode"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 流程节点名称
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 收购方式
class PurchaseType(db.Model):
    __tablename__ = "purchasetype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 流程节点名称
    Sequence = db.Column(db.String(1024))  # 流程顺序
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 仓库
class WareHouseType(db.Model):
    __tablename__ = "warehousetype"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 仓库名称
    Enabled = db.Column(db.Boolean)  # 是否启用
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 登记图片
class PictureRegister(db.Model):
    __tablename__ = "pictureregister"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Registers = db.relationship('Register', backref='Picture')


# 扦样图片
class PictureSample(db.Model):
    __tablename__ = "picturesample"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Samplings = db.relationship('Sampling', backref='Picture')


# 化验图片
class PictureAssay(db.Model):
    __tablename__ = "pictureassay"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 售粮图片
class PictureSell(db.Model):
    __tablename__ = "picturesell"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 检斤图片
class PictureWeigh(db.Model):
    __tablename__ = "pictureweigh"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    RoughPicture1 = db.Column(db.Text)  # 重检图片1
    RoughPicture2 = db.Column(db.Text)  # 重检图片2
    RoughPicture3 = db.Column(db.Text)  # 重检图片3
    RoughPicture4 = db.Column(db.Text)  # 重检图片4
    TarePicture1 = db.Column(db.Text)  # 空检图片1
    TarePicture2 = db.Column(db.Text)  # 空检图片2
    TarePicture3 = db.Column(db.Text)  # 空检图片3
    TarePicture4 = db.Column(db.Text)  # 空检图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 卸粮图片
class PictureUnload(db.Model):
    __tablename__ = "pictureunload"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 结算图片
class PictureSettlement(db.Model):
    __tablename__ = "picturesettlement"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Picture1 = db.Column(db.Text)  # 图片1
    Picture2 = db.Column(db.Text)  # 图片2
    Picture3 = db.Column(db.Text)  # 图片3
    Picture4 = db.Column(db.Text)  # 图片4
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间


# 售粮客户表
class Seller(db.Model):
    __tablename__ = "seller"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 名字
    IdentityID = db.Column(db.String(100), unique=True)  # 身份证号码
    Address = db.Column(db.String(100))  # 住址
    Phone = db.Column(db.String(100))  # 电话
    BankTypeID = db.Column(db.Integer, db.ForeignKey('banktype.ID'))  # 银行卡类型
    BankID = db.Column(db.String(100))  # 银行卡号
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Sellers = db.relationship('Register', backref='Seller', foreign_keys="Register.SellerID")
    Payees = db.relationship('Register', backref='Payee', foreign_keys="Register.PayeeID")
    Drivers = db.relationship('Register', backref='Driver', foreign_keys="Register.DriverID")


# 车辆管理表
class Vehicle(db.Model):
    __tablename__ = "vehicle"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Liscense = db.Column(db.String(100))  # 车牌号码
    VehicleTypeID = db.Column(db.Integer, db.ForeignKey('vehicletype.ID'))  # 车辆类型
    color = db.Column(db.String(100))  # 颜色
    FrameID = db.Column(db.String(100))  # 车架号码
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Registers = db.relationship('Register', backref='Vehicle', foreign_keys="Register.VehicleID")


# 计价方式
class Valuation(db.Model):
    __tablename__ = "valuation"
    ID = db.Column(db.Integer, primary_key=True)  # 编号
    Name = db.Column(db.String(100))  # 计价名称
    Price = db.Column(db.Float)  # 每吨多少钱
    IsDefault = db.Column(db.Boolean)  # 当前是否是核算的默认计价方式
    Detail = db.Column(db.Text)  # 详细计价方式内容
    Remarks = db.Column(db.String(1024))  # 备注
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Contracts = db.relationship('Contract', backref='Valuation', foreign_keys="Contract.ValuationID")


# 合同管理表
class Contract(db.Model):
    __tablename__ = "contract"
    ID = db.Column(db.Integer, primary_key=True)  # 合同编号
    ContractNum = db.Column(db.String(100))  # 合同号码
    ContractTypeID = db.Column(db.Integer, db.ForeignKey('contracttype.ID'))  # 合同类型
    StartTime = db.Column(db.DateTime)  # 开始日期
    EndTime = db.Column(db.DateTime)  # 结算日期
    OrderID = db.Column(db.String(100))  # 订单编号
    BankTypeID = db.Column(db.Integer, db.ForeignKey('banktype.ID'))  # 银行卡类型
    BankID = db.Column(db.String(100))  # 银行卡号
    TransportCompanyID = db.Column(db.Integer, db.ForeignKey('transportcompany.ID'))  # 运输公司ID
    TransportID = db.Column(db.String(100))  # 车船号码
    SupplierID = db.Column(db.Integer, db.ForeignKey('supplier.ID'))  # 供应商ID
    SourceAddress = db.Column(db.String(100))  # 原发地
    PurchaseAmount = db.Column(db.Integer)  # 采购总量
    PurchaseComplete = db.Column(db.Integer)  # 已完成总量
    PaymentTypeID = db.Column(db.Integer, db.ForeignKey('paymenttype.ID'))  # 支付方式
    WagonNum = db.Column(db.String(100))  # 车皮号码
    CerealsTypeID = db.Column(db.Integer, db.ForeignKey('cerealstype.ID'))  # 粮食类型
    ValuationID = db.Column(db.Integer, db.ForeignKey('valuation.ID'))  # 计价方式
    # Seller = db.Column(db.Integer, db.ForeignKey('seller.ID'))  # 联系人
    Contact = db.Column(db.String(100))  # 联系人
    ContactPhone = db.Column(db.String(100))  # 联系人电话
    IsComplete = db.Column(db.Boolean)  # 是否完成
    Remarks = db.Column(db.String(1024))  # 备注
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Registers = db.relationship('Register', backref='Contract', foreign_keys="Register.ContractID")


# 登记表
class Register(db.Model):
    __tablename__ = "register"
    ID = db.Column(db.Integer, primary_key=True)  # 凭证号
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.ID'))  # 车辆ID
    PurchaseType = db.Column(db.String(100))  # 收购流程
    PaymentTypeID = db.Column(db.Integer, db.ForeignKey('paymenttype.ID'))  # 支付方式
    PackTypeID = db.Column(db.Integer, db.ForeignKey('packtype.ID'))  # 包装方式
    CerealsTypeID = db.Column(db.Integer, db.ForeignKey('cerealstype.ID'))  # 粮食类型
    SellerID = db.Column(db.Integer, db.ForeignKey('seller.ID'))  # 售粮人
    PayeeID = db.Column(db.Integer, db.ForeignKey('seller.ID'))  # 结算人
    DriverID = db.Column(db.Integer, db.ForeignKey('seller.ID'))  # 司机
    ContractID = db.Column(db.Integer, db.ForeignKey('contract.ID'))  # 合同号码
    TagNum = db.Column(db.String(100))  # 电子标签号码
    TagStatus = db.Column(db.String(100))  # 电子标签状态
    ICID = db.Column(db.String(100))  # IC卡号码
    Remarks = db.Column(db.String(1024))  # IC卡号码
    PirctureID = db.Column(db.Integer, db.ForeignKey('pictureregister.ID'))  # 图片信息
    IsComplete = db.Column(db.String(32))  # 收购流程是否完成  'OC'= 完成 'FZ' = 冻结 'BE'= 进行中 'IT' = 中断退出
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Register')
    Samplings = db.relationship('Sampling', backref='Register')
    Assays = db.relationship('Assay', backref='Register')
    Sells = db.relationship('Sell', backref='Register')
    Weighs = db.relationship('Weigh', backref='Register')
    Unloads = db.relationship('Unload', backref='Register')
    Settlements = db.relationship('Settlement', backref='Register')


# 扦样表
class Sampling(db.Model):
    __tablename__ = "sampling"
    ID = db.Column(db.Integer, primary_key=True)  # 扦样编号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    PirctureID = db.Column(db.Integer, db.ForeignKey('picturesample.ID'))  # 图片信息
    Remarks = db.Column(db.String(1024))  # 备注信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Sampling')


# 化验表
class Assay(db.Model):
    __tablename__ = "assay"
    ID = db.Column(db.Integer, primary_key=True)  # 化验单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    CerealsTypeID = db.Column(db.Integer, db.ForeignKey('cerealstype.ID'))  # 粮食类型
    SampleClassID = db.Column(db.Integer, db.ForeignKey('sampleclass.ID'))  # 样品级别
    SampleBox = db.Column(db.String(100))  # 样品盒号码
    IsStandard = db.Column(db.Boolean)  # 是否是标准样
    UnitWeight = db.Column(db.Float)  # 容重
    Moisture = db.Column(db.Float)  # 水分
    Mildew = db.Column(db.Float)  # 霉变
    Broken = db.Column(db.Float)  # 破损
    HeatHarm = db.Column(db.Float)  # 热损
    SideImpurity = db.Column(db.Float)  # 并间杂
    Scree = db.Column(db.Float)  # 小石子
    SoilBlock = db.Column(db.Float)  # 土块
    RodCore = db.Column(db.Float)  # 棒芯
    DifferentGrain = db.Column(db.Float)  # 异种粮
    BlistersGrain = db.Column(db.Float)  # 水泡粒
    PeculiarSmell = db.Column(db.Boolean)  # 异味
    RoughWeight = db.Column(db.Float)  # 样品毛重
    NetWeight = db.Column(db.Float)  # 样品净重
    Impurity = db.Column(db.Float)  # 杂志
    IsComplete = db.Column(db.Boolean)  # 是否化验完毕
    IsReject = db.Column(db.Boolean)  # 是否拒收
    RejectContent = db.Column(db.String(1024))  # 拒收原因
    Reserved = db.Column(db.String(1024))  # 留样号码
    Remarks = db.Column(db.String(1024))  # 备注信息
    PirctureID = db.Column(db.Integer, db.ForeignKey('pictureassay.ID'))  # 图片信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 更新时间
    Procedures = db.relationship('Procedure', backref='Assay')


# 售粮表
class Sell(db.Model):
    __tablename__ = "sell"
    ID = db.Column(db.Integer, primary_key=True)  # 售粮单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    IsSell = db.Column(db.Boolean)  # 是否出售
    PirctureID = db.Column(db.Integer, db.ForeignKey('picturesell.ID'))  # 图片信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Sell')


# 检斤表
class Weigh(db.Model):
    __tablename__ = "weigh"
    ID = db.Column(db.Integer, primary_key=True)  # 检斤单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.ID'))  # 车辆ID
    RoughWeight = db.Column(db.Float)  # 毛重
    RoughDate = db.Column(db.DateTime)  # 毛重时间
    TareWeight = db.Column(db.Float)  # 皮重
    TareDate = db.Column(db.DateTime)  # 皮重时间
    NetWeight = db.Column(db.Float)  # 净重
    PirctureID = db.Column(db.Integer, db.ForeignKey('pictureweigh.ID'))  # 图片信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Weigh')


# 卸车表
class Unload(db.Model):
    __tablename__ = "unload"
    ID = db.Column(db.Integer, primary_key=True)  # 卸货单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.ID'))  # 车辆ID
    TakeWeight = db.Column(db.Float)  # 扣重量
    WarehouseType = db.Column(db.Integer, db.ForeignKey('warehousetype.ID'))  # 仓库类型
    PirctureID = db.Column(db.Integer, db.ForeignKey('pictureunload.ID'))  # 图片信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Unload')


# 结算表
class Settlement(db.Model):
    __tablename__ = "settlement"
    ID = db.Column(db.Integer, primary_key=True)  # 结算单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))  # 登记表ID
    ValuationID = db.Column(db.Integer, db.ForeignKey('valuation.ID'))  # 计价方式
    UnitPrice = db.Column(db.Float)  # 单价
    TotalPrice = db.Column(db.Float)  # 总价
    IsPayment = db.Column(db.Boolean)  # 是否付款
    PirctureID = db.Column(db.Integer, db.ForeignKey('picturesettlement.ID'))  # 图片信息
    CreateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 创建者
    CreateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    UpdateID = db.Column(db.Integer, db.ForeignKey('user.ID'))  # 更新者
    UpdateTime = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    Procedures = db.relationship('Procedure', backref='Settlement')


# 流程表
class Procedure(db.Model):
    __tablename__ = "procedure"
    ID = db.Column(db.Integer, primary_key=True)  # 结算单号
    RegisterID = db.Column(db.Integer, db.ForeignKey('register.ID'))
    SamplingID = db.Column(db.Integer, db.ForeignKey('sampling.ID'))
    AssayID = db.Column(db.Integer, db.ForeignKey('assay.ID'))
    SellID = db.Column(db.Integer, db.ForeignKey('sell.ID'))
    WeighID = db.Column(db.Integer, db.ForeignKey('weigh.ID'))
    UnloadID = db.Column(db.Integer, db.ForeignKey('unload.ID'))
    SettlementID = db.Column(db.Integer, db.ForeignKey('settlement.ID'))
    CurrentNode = db.Column(db.String(100))
    IsFrozen = db.Column(db.Integer)
    FrozenerID = db.Column(db.Integer, db.ForeignKey('user.ID'))













