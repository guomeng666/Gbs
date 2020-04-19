from app.models import *
import json


# 处理客户端查询的角色数据
def query_role(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    role_name = json_data.get("RoleName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, role_name, start_page, per_page, start_date, end_date)
    role_name.strip()
    if len(role_name) != 0:
        # result = db.session.query(Role.ID, Role.Name, Role.Primissions, Role.CreateTime, Role.UpdateTime)
        # print("result:", result.count())
        page_data = Role.query.filter(Role.Name == role_name).\
            paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = Role.query.filter(Role.CreateTime.between(start_date, end_date)) \
            .order_by(Role.CreateTime.desc()) \
            .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Role.query.order_by(Role.CreateTime.desc()).paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for role in page_data.items:
        row = {"ID": role.ID, "Name": role.Name, "Permission": "",
               "CreateTime": str(role.CreateTime), "UpdateTime": str(role.UpdateTime)}
        query_list.append(row)
        print(role.Primissions)
    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 角色编辑接口
def edit_role(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    operation = json_data.get("Operation")
    role_number = json_data.get("Number")
    role_name = json_data.get("RoleName")
    permission_number = json_data.get("PrimissionID")

    if operation == "alter":
        # 数据存在才可以修改
        alter_role = Role.query.filter(Role.ID == role_number).first()
        if alter_role:
            alter_permission = Primisson.query.filter(Primisson.ID == permission_number).first()
            if alter_permission:
                alter_role.Name = role_name
                alter_role.UpdateTime = datetime.now()
                db.session.add(alter_role)
                db.session.commit()
                result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                          "TotalData": "", "Data": ""}
            else:
                result = {"Cmd": cmd, "Errno": 5, "ErrMsg": "The modify data option has been deleted", "Page": "",
                          "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_role = Role.query.filter_by(Name=role_name).first()
        # 数据没有重名的可以添加
        if not old_role:
            new_role = Role(Name=role_name)
            db.session.add(new_role)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "delete":
        # 先查询删除的数据是否存在
        delete_role = Primisson.query.filter(Role.ID == role_number).first()
        if delete_role:
            db.session.delete(delete_role)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询权限接口
def query_permission(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    permission_name = json_data.get("PermissionName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, permission_name, start_page, per_page, start_date, end_date)
    permission_name.strip()
    if len(permission_name) != 0:
        print("if")
        page_data = Primisson.query.filter(Primisson.Name == permission_name).\
            paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        print("elif")
        page_data = Primisson.query.filter(Primisson.CreateTime.between(start_date, end_date)) \
            .order_by(Primisson.CreateTime.desc()) \
            .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Primisson.query.order_by(Primisson.CreateTime.desc())\
            .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for primisson in page_data.items:
        row = {"ID": primisson.ID, "Name": primisson.Name, "Quer": primisson.Quer,
               "Maintain": primisson.Maintain, "Register": primisson.Register,
               "Sampling": primisson.Sampling, "Assay": primisson.Assay,
               "Sell": primisson.Sell, "Weigh": primisson.Weigh,
               "Unload": primisson.Unload, "Settlement": primisson.Settlement,
               "CreateTime": str(primisson.CreateTime), "UpdateTime": str(primisson.UpdateTime)}
        query_list.append(row)
        print(primisson.Primissions)
    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 权限编辑接口
def edit_permission(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    operation = json_data.get("Operation")
    permission_name = json_data.get("PermissionName")
    permission_number = json_data.get("Number")
    query_permission_bits = json_data.get("QueryPri")
    maintain_permission_bits = json_data.get("MaintainPri")
    register_permission_bits = json_data.get("AlterRegisterPri")
    sampling_permission_bits = json_data.get("AlterSamplingPri")
    assay_permission_bits = json_data.get("AlterAssayPri")
    sell_permission_bits = json_data.get("AlterSellPri")
    weigh_permission_bits = json_data.get("AlterWeighPri")
    unload_permission_bits = json_data.get("AlterUnloadPri")
    settlement_permission_bits = json_data.get("AlterSettlementPri")

    if operation == "alter":
        # 数据存在可以修改
        alter_primisson = Primisson.query.filter(Primisson.ID == permission_number).first()
        if alter_primisson:
            alter_primisson.Name = permission_name
            alter_primisson.Quer = query_permission_bits
            alter_primisson.Maintain = maintain_permission_bits
            alter_primisson.Register = register_permission_bits
            alter_primisson.Sampling = sampling_permission_bits
            alter_primisson.Assay = assay_permission_bits
            alter_primisson.Sell = sell_permission_bits
            alter_primisson.Weigh = weigh_permission_bits
            alter_primisson.Unload = unload_permission_bits
            alter_primisson.Settlement = settlement_permission_bits
            alter_primisson.UpdateTime = datetime.now()
            db.session.add(alter_primisson)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_perssion = Primisson.query.filter_by(Name=permission_name).first()
        # 数据没有重名的可以添加
        if not old_perssion:
            new_permission = Primisson(Name=permission_name, Quer=query_permission_bits,
                                       Maintain=maintain_permission_bits, Register=register_permission_bits,
                                       Sampling=sampling_permission_bits, Assay=assay_permission_bits,
                                       Sell=sell_permission_bits, Weigh=weigh_permission_bits,
                                       Unload=unload_permission_bits, Settlement=settlement_permission_bits)
            db.session.add(new_permission)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "delete":
        # 先查询删除的数据是否存在
        delete_primisson = Primisson.query.filter(Primisson.ID == permission_number).first()
        if delete_primisson:
            db.session.delete(delete_primisson)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)
