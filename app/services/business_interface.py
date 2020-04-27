from app.models import *
import json


def add_vehicle(vehicle_liscense, vehicle_type_id, vehicle_color, vehicle_frame, operator):
    vehicle = Vehicle.query.filter(Vehicle.Liscense == vehicle_liscense).first()
    if not vehicle:
        vehicle_type = VehicleType.query.filter(VehicleType.ID == vehicle_type_id).first()
        vehicle = Vehicle(Liscense=vehicle_liscense)
        vehicle.color = vehicle_color
        vehicle.FrameID = vehicle_frame
        vehicle.VehicleType = vehicle_type
        vehicle.Creater = operator
        vehicle.Updater = operator
        db.session.add(vehicle)
        db.session.commit()
    return vehicle


def add_seller(name, num, address, phone, banktype, bank_num, operator):
    seller = Seller.query.filter_by(Name=name).first()
    # 数据没有重名的可以添加
    if not seller:
        seller = Seller(Name=name)
        seller.IdentityID = num
        seller.Address = address
        seller.Phone = phone
        if banktype:
            seller.BankType = banktype
        seller.BankID = bank_num
        seller.Creater = operator
        seller.Updater = operator
        db.session.add(seller)
        db.session.commit()
    return seller


# 查询图片
def query_picture(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    picture_id = json_data.get("Number")
    node = json_data.get("Node")

    if node == "Register":
        picture = PictureRegister.query.filter(PictureRegister.ID == picture_id).first()

    if picture:
        row = {
            "Picture1": picture.Picture1, "Picture2": picture.Picture2,
            "Picture3": picture.Picture3, "Picture4": picture.Picture4,
              }
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": 0,
                  "TotalData": "", "Data": row}
    else:
        result = {"Cmd": cmd, "Errno": 8, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}

    return json.dumps(result)


# 使用身份证号码查询信息
def query_seller_by_identityid(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    identity_id = json_data.get("IdentityID")
    page_data = Seller.query.filter(Seller.IdentityID == identity_id) \
        .paginate(page=int(1), per_page=int(20))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页

    if page_data.total != 0:
        for seller in page_data.items:
            if seller.BankType:
                bank_name = seller.BankType.Name
            else:
                bank_name = ""
            row = {
                "ID": seller.ID, "Name": seller.Name, "IdentityID": seller.IdentityID, "Address": seller.Address,
                "Phone": seller.Phone, "BankType": bank_name, "BankID": seller.BankID,
                "Creater": seller.Creater.Name, "Updater": seller.Updater.Name,
                "CreateTime": str(seller.CreateTime), "UpdateTime": str(seller.UpdateTime)
            }
            query_list.append(row)

            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": 1,
                      "TotalData": page_data.total, "Data": query_list}
    else:
        result = {"Cmd": cmd, "Errno": 8, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}

    return json.dumps(result)


# 查询登记信息
def query_register(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    field = json_data.get("Field")
    name = json_data.get("Name")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    name.strip()
    if len(name) != 0:
        # 按车牌号码查询数据
        if field == "车牌号码":
            # 先根据车牌号码查询车辆信息
            vehicle = Vehicle.query.filter(Vehicle.Liscense == name).first()
            page_data = Register.query.filter(Register.Vehicle == vehicle)\
                .paginate(page=int(start_page), per_page=int(per_page))

    elif start_date and end_date is not None:
        page_data = Register.query.filter(Register.CreateTime.between(start_date, end_date)) \
                    .order_by(Register.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Register.query.order_by(Register.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页

    for register in page_data.items:
        seller_name = ""
        seller_num = ""
        seller_address = ""
        seller_phone = ""

        payee_name = ""
        payee_num = ""
        payee_address = ""
        payee_phone = ""
        payee_bank_type = ""
        payee_bank_num = ""

        driver_name = ""
        driver_num = ""
        driver_address = ""
        driver_phone = ""
        picture = ""
        pay_type = ""
        contract_num = ""

        if register.Driver:
            driver_name = register.Driver.Name
            driver_num = register.Driver.IdentityID
            driver_address = register.Driver.Address
            driver_phone = register.Driver.Phone
        if register.Seller:
            seller_name = register.Seller.Name
            seller_num = register.Seller.IdentityID
            seller_address = register.Seller.Address
            seller_phone = register.Seller.Phone
        if register.Payee:
            payee_name = register.Payee.Name
            payee_num = register.Payee.IdentityID
            payee_address = register.Payee.Address
            payee_phone = register.Payee.Phone
            if register.Payee.BankType:
                payee_bank_type = register.Payee.BankType.Name
                payee_bank_num = register.Payee.BankID
        if register.PirctureID:
            picture = register.Picture.ID
        if register.PaymentType:
            pay_type = register.PaymentType.Name
        if register.Contract:
            contract_num = register.Contract.ContractNum
        row = {
               "ID": register.ID, "PurchaseType": register.PurchaseType, "ContractNum": contract_num,
               "GrainType": register.CerealsType.Name,
               "PackType": register.PackType.Name,  "Pay": pay_type, "TagNum": register.TagNum,
               "ICNum": register.ICID, "License": register.Vehicle.Liscense,
               "VehicleType": register.Vehicle.VehicleType.Name, "Color": register.Vehicle.color,
               "Frame": register.Vehicle.FrameID,
               "SellerName": seller_name, "SellerNum": seller_num,
               "SellerAddress": seller_address, "SellerPhone": seller_phone,
               "PayeeName": payee_name, "PayeeNum": payee_num,
               "PayeeAddress": payee_address, "PayeePhone": payee_phone,
               "BankType": payee_bank_type, "BankNum": payee_bank_num,
               "DriverName": driver_name, "DriverNum": driver_num,
               "DriverAddress": driver_address, "DriverPhone": driver_phone,
               "Remark": register.Remarks, "PrictureID": picture,
               "Creater": register.Creater.Name, "Updater": register.Updater.Name,
               "CreateTime": str(register.CreateTime), "UpdateTime": str(register.UpdateTime)
               }
        query_list.append(row)
    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    print(result)
    return json.dumps(result)


# 编辑登记信息
def edit_register(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    number = json_data.get("Number")                     # 数据库编号 修改使用
    purchase_type = json_data.get("PurchaseType")            # 收购流程
    contract_num = json_data.get("ContractNum")          # 合同号码
    vehicle_liscense = json_data.get("VehicleLiscence")  # 车牌号码
    vehicle_type_id = json_data.get("VehicleType")          # 车辆类型
    vehicle_color = json_data.get("VehicleColor")        # 车辆颜色
    vehicle_frame = json_data.get("VehicleFrameId")      # 车架号码
    driver_num = json_data.get("DriverNum")              # 司机证件号码
    driver_name = json_data.get("DriverName")            # 司机名字
    driver_address = json_data.get("DriverAddress")      # 司机住址
    driver_phone = json_data.get("DriverPhone")          # 司机电话
    seller_num = json_data.get("SellerNum")              # 售粮人证件号码
    seller_name = json_data.get("SellerName")            # 售粮人名字
    seller_address = json_data.get("SellerAddress")      # 售粮人住址
    seller_phone = json_data.get("SellerPhone")          # 售粮人电话
    payee_num = json_data.get("PayeeNum")                # 收款人证件号码
    payee_name = json_data.get("PayeeName")              # 收款人姓名
    payee_address = json_data.get("PayeeAddress")        # 收款人住址
    payee_phone = json_data.get("PayeePhone")            # 收款人电话
    bank_type_id = json_data.get("PayeeBankType")     # 收款人银行类型
    bank_num = json_data.get("PayeeBankNum")       # 收款人银行号
    payment_type_id = json_data.get("PayMentType")          # 支付方式
    pack_type_id = json_data.get("PackType")                # 包装类型
    grain_type_id = json_data.get("GrainType")              # 粮食类型
    tag_num = json_data.get("TagNum")                    # 电子标签号码
    tag_status = json_data.get("TagStatus")              # 电子标签状态
    icid = json_data.get("ICID")                         # IC卡号码
    remarks = json_data.get("Remarks")                   # 备注
    pircture1 = json_data.get("Pircture1")              # 图片1
    pircture2 = json_data.get("Pircture2")              # 图片2
    pircture3 = json_data.get("Pircture3")              # 图片3
    pircture4 = json_data.get("Pircture4")              # 图片4

    # 获取发送人
    operator = User.query.filter(User.Name == sender).first()
    # 添加车辆信息,必须存在
    vehicle = add_vehicle(vehicle_liscense=vehicle_liscense, vehicle_type_id=vehicle_type_id,
                          vehicle_color=vehicle_color, vehicle_frame=vehicle_frame,
                          operator=operator)
    # 银行类型
    bank_type = BankType.query.filter(BankType.ID == bank_type_id).first()
    grain_type = CerealsType.query.filter(CerealsType.ID == grain_type_id).first()
    pack_type = PakeType.query.filter(PakeType.ID == pack_type_id).first()
    payment_type = PaymentType.query.filter(PaymentType.ID == payment_type_id).first()

    if operation == "alter" or operation == "add":
        if operation == "alter":
            # 修改则需要找出旧记录
            register = Register.query.filter(Register.ID == number).first()
        else:
            # 增加新建记录
            register = Register()
        if purchase_type == "散收粮":
            # 散收粮需要添加售粮人,结算人信息
            register.Seller = add_seller(seller_name, seller_num, seller_address,
                                         seller_phone, bank_type, bank_num, operator)
            register.Payee = add_seller(payee_name, payee_num, payee_address,
                                        payee_phone, bank_type, bank_num, operator)
            register.PaymentType = payment_type  # 支付方式
        else:
            # 合同粮需要添加合同号,司机信息
            register.Contract = Contract.query.filter(Contract.ContractNum == contract_num).first()
            register.Driver = add_seller(driver_name, driver_num, driver_address,
                                         driver_phone, bank_type, bank_num, operator)

        # 如果是新建立则把图片存起来
        if operation == "add":
            pircture = PictureRegister()
            pircture.Picture1 = pircture1
            pircture.Picture2 = pircture2
            pircture.Picture3 = pircture3
            pircture.Picture4 = pircture4
            pircture.Creater = operator
            pircture.Updater = operator
            db.session.add(pircture)
            db.session.commit()
            register.Picture = pircture  # 图片信息

        register.PurchaseType = purchase_type
        register.Vehicle = vehicle  # 车辆信息ID
        register.PurchaseType = purchase_type  # 收购流程
        register.PackType = pack_type  # 包装类型ID
        register.CerealsType = grain_type  # 粮食类型ID

        register.TagNum = tag_num  # 标签号码
        register.TagStatus = tag_status  # 标签状态
        register.ICID = icid  # IC卡号
        register.Remarks = remarks  # 备注信息
        if operation == "add":
            register.Creater = operator
        register.Updater = operator
        db.session.add(register)
        db.session.commit()
        if operation == "add":
            # 把新建立的登记数据放入到流程表中
            procedure = Procedure()
            procedure.Register = register
            db.session.add(procedure)
            db.session.commit()

        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    elif operation == "delete":
        # 先查询删除的数据是否存在
        delete = Register.query.filter(Register.ID == number).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)

