from app.models import *
import json


def add_vehicle(vehicle_liscense, vehicle_type_id, vehicle_color, vehicle_frame, operator):
    vehicle = Vehicle.query.filter(Vehicle.Liscense == vehicle_liscense).first()
    if not vehicle:
        vehicle_type = ContractType.query.filter(VehicleType.ID == vehicle_type_id).first()
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
        seller.BankType = banktype
        seller.BankID = bank_num
        seller.Creater = operator
        seller.Updater = operator
        db.session.add(seller)
        db.session.commit()
    return seller


# 查询登记信息
def query_register(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    name = json_data.get("Name")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, name, start_page, per_page, start_date, end_date)
    name.strip()
    if len(name) != 0:
        page_data = Contract.query.filter(Contract.ContractNum == name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = Contract.query.filter(Contract.CreateTime.between(start_date, end_date)) \
                    .order_by(Contract.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Contract.query.order_by(Contract.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for contract in page_data.items:
        row = {
               "ID": contract.ID, "ContractNum": contract.ContractNum, "ContractType": contract.ContractType.Name,
               "GrainType": contract.CerealsType.Name, "Start": str(contract.StartTime), "End": str(contract.EndTime),
               "OrderID": contract.OrderID, "Supplier": contract.Supplier.Name,
               "TransCompany": contract.TransprotCompany.Name, "Source": contract.SourceAddress,
               "Total": contract.PurchaseAmount, "Complete": contract.PurchaseComplete,
               "TransportNum": contract.TransportID, "WagaonNum": contract.WagonNum,
               "PayType": contract.PaymentType.Name, "BankType": contract.BankType.Name,
               "BankNum": contract.BankID, "Contact": contract.Contact,
               "ContactPhone": contract.ContactPhone, "IsComplete": contract.IsComplete,
               "Remark": contract.Remarks, "Valuation": contract.Valuation.Name,
               "Creater": contract.Creater.Name, "Updater": contract.Updater.Name,
               "CreateTime": str(contract.CreateTime), "UpdateTime": str(contract.UpdateTime)
               }
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑登记信息
def edit_register(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    number = json_data.get("Number")                     # 数据库编号 修改使用
    purchase_id = json_data.get("PurchaseID")            # 收购流程
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

    # 获取发送人
    operator = User.query.filter(User.Name == sender).first()

    # 查询所有外键
    bank_type = BankType.query.filter(BankType.ID == bank_type_id).first()
    grain_type = CerealsType.query.filter(CerealsType.ID == grain_type_id).first()
    pack_type = PakeType.query.filter(PakeType.ID == pack_type_id).first()
    payment_type = PaymentType.query.filter(PaymentType.ID == payment_type_id).first()

    # 添加车辆信息
    vehicle = add_vehicle(vehicle_liscense=vehicle_liscense, vehicle_type_id=vehicle_type_id,
                          vehicle_color=vehicle_color, vehicle_frame=vehicle_frame,
                          operator=operator)

    seller = add_seller(seller_name, seller_num, seller_address,
                        seller_phone, bank_type, bank_num, operator)

    payee = add_seller(payee_name, payee_num, payee_address,
                       payee_phone, bank_type, bank_num, operator)

    driver = add_seller(driver_name, driver_num, driver_address,
                        driver_phone, bank_type, bank_num, operator)

    operator = User.query.filter(User.Name == sender).first()

    if operation == "alter":
        # 数据存在才可以修改
        alter = Register.query.filter(Register.ID == number).first()
        if alter:
            alter.Vehicle = vehicle   # 车辆信息ID
            alter.PurchaseType = purchase_id  # 收购流程
            alter.PackType = pack_type  # 包装类型ID
            alter.CerealsType = grain_type  # 粮食类型ID
            alter.SellerID = seller  # 售粮人ID
            alter.PayeeID = payee  # 结算人类型ID
            alter.DriverID = driver  # 司机ID
            alter.PaymentType = payment_type  # 结算方式ID
            alter.ContractID = contract_num  # 合同号码
            alter.TagNum = tag_num  # 标签号码
            alter.TagStatus = tag_status  # 标签状态
            alter.ICID = icid  # IC卡号
            alter.Remarks = remarks  # 备注信息
            alter.PirctureID = ""    # 图片信息

            alter.Updater = operator
            alter.UpdateTime = datetime.now()
            db.session.add(alter)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        # 增加记录
        new = Register()
        new.Vehicle = vehicle  # 车辆信息ID
        new.PurchaseType = purchase_id  # 收购流程
        new.PackType = pack_type  # 包装类型ID
        new.CerealsType = grain_type  # 粮食类型ID
        new.SellerID = seller  # 售粮人ID
        new.PayeeID = payee  # 结算人类型ID
        new.DriverID = driver  # 司机ID
        new.PaymentType = payment_type  # 结算方式ID
        new.ContractID = contract_num  # 合同号码
        new.TagNum = tag_num  # 标签号码
        new.TagStatus = tag_status  # 标签状态
        new.ICID = icid  # IC卡号
        new.Remarks = remarks  # 备注信息
        new.PirctureID = ""  # 图片信息

        new.Creater = operator
        new.Updater = operator

        db.session.add(new)
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

