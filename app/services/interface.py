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

    role_name.strip()
    if len(role_name) != 0:
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
        if role.Permissons is not None:
            row = {"ID": role.ID, "Name": role.Name, "Permission": role.Permissons.Name,
                   "CreateTime": str(role.CreateTime), "UpdateTime": str(role.UpdateTime)}
        else:
            row = {"ID": role.ID, "Name": role.Name, "Permission": "",
                   "CreateTime": str(role.CreateTime), "UpdateTime": str(role.UpdateTime)}
        query_list.append(row)

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

    permission = Primisson.query.filter(Primisson.ID == permission_number).first()
    if permission:
        if operation == "alter":
            # 数据存在才可以修改
            alter_role = Role.query.filter(Role.ID == role_number).first()
            if alter_role:
                alter_role.Name = role_name
                alter_role.Permissons = permission
                alter_role.UpdateTime = datetime.now()
                db.session.add(alter_role)
                db.session.commit()
                result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                          "TotalData": "", "Data": ""}
            else:
                result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                          "TotalData": "", "Data": ""}
        elif operation == "add":
            old_role = Role.query.filter_by(Name=role_name).first()
            # 数据没有重名的可以添加
            if not old_role:
                new_role = Role(Name=role_name)
                new_role.Permissons = permission
                db.session.add(new_role)
                db.session.commit()
                result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                          "TotalData": "", "Data": ""}
            else:
                # 数据重名了
                result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                          "TotalData": "", "Data": ""}
    else:
        if operation == "delete":
            # 先查询删除的数据是否存在
            delete_role = Role.query.filter(Role.ID == role_number).first()
            if delete_role:
                db.session.delete(delete_role)
                db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 选择项不存在,应该是被删除了
            result = {"Cmd": cmd, "Errno": 5, "ErrMsg": "The modify data option has been deleted", "Page": "",
                      "TotalData": "", "Data": ""}
    return json.dumps(result)


# 权限查询接口
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
        page_data = Primisson.query.filter(Primisson.Name == permission_name).\
            paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
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


# 查询部门数据
def query_department(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    department_name = json_data.get("DepartmentName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, department_name, start_page, per_page, start_date, end_date)
    department_name.strip()
    if len(department_name) != 0:
        page_data = Department.query.filter(Department.Name == department_name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = Department.query.filter(Department.CreateTime.between(start_date, end_date)) \
                    .order_by(Department.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Department.query.order_by(Department.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for department in page_data.items:
        row = {"ID": department.ID, "Name": department.Name, "CreateTime": str(department.CreateTime),
               "UpdateTime": str(department.UpdateTime)}
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑部门数据
def edit_department(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    operation = json_data.get("Operation")
    department_number = json_data.get("Number")
    department_name = json_data.get("DepartmentName")

    if operation == "alter":
        # 数据存在才可以修改
        alter_department = Department.query.filter(Department.ID == department_number).first()
        if alter_department:
            alter_department.Name = department_name
            alter_department.UpdateTime = datetime.now()
            db.session.add(alter_department)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_department = Department.query.filter_by(Name=department_name).first()
        # 数据没有重名的可以添加
        if not old_department:
            new_department = Department(Name=department_name)
            db.session.add(new_department)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete_department = Department.query.filter(Department.ID == department_number).first()
        if delete_department:
            db.session.delete(delete_department)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询用户数据接口
def query_user(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    user_name = json_data.get("UserName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, user_name, start_page, per_page, start_date, end_date)
    user_name.strip()
    if len(user_name) != 0:
        page_data = User.query.filter(User.Name == user_name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = User.query.filter(User.CreateTime.between(start_date, end_date)) \
                    .order_by(User.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = User.query.order_by(User.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for user in page_data.items:
        user_roles = list()
        for role in user.Roles:
            user_roles.append(role.Name)
        row = {"ID": user.ID, "Name": user.Name, "Password": user.PasswordHash, "IdentityID": user.IdentityID,
               "Address": user.Address, "Department": user.Department.Name, "LastLoginTime": str(user.LastLoginTime),
               "Roles": ','.join(user_roles), "CreateTime": str(user.CreateTime),
               "UpdateTime": str(user.UpdateTime)}
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 用户编辑接口
def edit_user(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    operation = json_data.get("Operation")
    user_number = json_data.get("Number")
    user_name = json_data.get("UserName")
    user_password = json_data.get("UserPassword")
    user_identity = json_data.get("UserIdentityID")
    user_address = json_data.get("UserAddress")
    user_roles_id = json_data.get("UserRoleID")
    user_department_id = json_data.get("UserDepartmentID")
    user_roles_list = user_roles_id.split(',')

    alter_user = User.query.filter(User.ID == user_number).first()
    alter_department = Department.query.filter(Department.ID == user_department_id).first()
    if operation == "alter":
        # 数据存在才可以修改
        if alter_user:
            alter_user.Name = user_name
            alter_user.password = user_password
            alter_user.IdentityID = user_identity
            alter_user.Address = user_address
            if alter_department:
                alter_user.Department = alter_department
            for remove_role in alter_user.Roles:
                alter_user.Roles.remove(remove_role)
            for role_id in user_roles_list:
                alter_role = Role.query.filter(Role.ID == role_id).first()
                # 修改的角色是不是已经有了
                if alter_role not in alter_user.Roles:
                    alter_user.Roles.append(alter_role)
            alter_user.UpdateTime = datetime.now()
            db.session.add(alter_user)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 修改的数据不存在
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "The modify data option has been deleted", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_department = User.query.filter_by(Name=user_name).first()
        # 数据没有重名的可以添加
        if not old_department:
            new_department = User()
            new_department.Name = user_name
            new_department.password = user_password
            new_department.IdentityID = user_identity
            new_department.Address = user_address
            if alter_department:
                new_department.Department = alter_department
            # 修改角色
            for role_id in user_roles_list:
                alter_role = Role.query.filter(Role.ID == role_id).first()
                if alter_role:
                    new_department.Roles.append(alter_role)

            new_department.UpdateTime = datetime.now()
            db.session.add(new_department)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据已经存在
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete_user = User.query.filter(User.ID == user_number).first()
        if delete_user:
            db.session.delete(delete_user)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询车辆类型数据
def query_vehicletype(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    vehicle_type_name = json_data.get("VehicleTypeName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, vehicle_type_name, start_page, per_page, start_date, end_date)
    vehicle_type_name.strip()
    if len(vehicle_type_name) != 0:
        page_data = VehicleType.query.filter(VehicleType.Name == vehicle_type_name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = VehicleType.query.filter(VehicleType.CreateTime.between(start_date, end_date)) \
                    .order_by(VehicleType.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = VehicleType.query.order_by(VehicleType.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for vehicle_type in page_data.items:
        row = {"ID": vehicle_type.ID, "Name": vehicle_type.Name,  "EstimateLoad": vehicle_type.EstimateLoad,
               "Creater": vehicle_type.Creater.Name, "Updater": vehicle_type.Updater.Name,
               "CreateTime": str(vehicle_type.CreateTime), "UpdateTime": str(vehicle_type.UpdateTime)}
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑车辆类型数据
def edit_vehicletype(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    vehicletype_number = json_data.get("Number")
    vehicletype_name = json_data.get("VehicleTypeName")
    estimateload = json_data.get("EstimateLoad")

    operator = User.query.filter(User.Name == sender).first()
    if operation == "alter":
        # 数据存在才可以修改
        alter_vehicletype = VehicleType.query.filter(VehicleType.ID == vehicletype_number).first()
        if alter_vehicletype:
            alter_vehicletype.Name = vehicletype_name
            alter_vehicletype.EstimateLoad = estimateload
            alter_vehicletype.Updater = operator
            alter_vehicletype.UpdateTime = datetime.now()
            db.session.add(alter_vehicletype)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_vehicletype = VehicleType.query.filter_by(Name=vehicletype_name).first()
        # 数据没有重名的可以添加
        if not old_vehicletype:
            new_vehicletype = VehicleType(Name=vehicletype_name)
            new_vehicletype.EstimateLoad = estimateload
            new_vehicletype.Creater = operator
            new_vehicletype.Updater = operator
            db.session.add(new_vehicletype)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete_vehicletype = VehicleType.query.filter(VehicleType.ID == vehicletype_number).first()
        if delete_vehicletype:
            db.session.delete(delete_vehicletype)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询车辆数据
def query_vehicle(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    vehicle_name = json_data.get("VehicleLiscence")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, vehicle_name, start_page, per_page, start_date, end_date)
    vehicle_name.strip()
    if len(vehicle_name) != 0:
        page_data = Vehicle.query.filter(Vehicle.Liscense == vehicle_name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = Vehicle.query.filter(Vehicle.CreateTime.between(start_date, end_date)) \
                    .order_by(Vehicle.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Vehicle.query.order_by(Vehicle.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for vehicle in page_data.items:
        row = {"ID": vehicle.ID, "Name": vehicle.Liscense,  "VehicleType": vehicle.VehicleType.Name,
               "color": vehicle.color, "FrameID": vehicle.FrameID,
               "Creater": vehicle.Creater.Name, "Updater": vehicle.Updater.Name,
               "CreateTime": str(vehicle.CreateTime), "UpdateTime": str(vehicle.UpdateTime)}
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑车辆数据
def edit_vehicle(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    vehicle_number = json_data.get("Number")
    vehicle_liscence = json_data.get("VehicleLiscence")
    vehicle_type = json_data.get("VehicleType")
    vehicle_color = json_data.get("VehicleColor")
    vehicle_frame_id = json_data.get("VehicleFrameId")
    operator = User.query.filter(User.Name == sender).first()
    if operation == "alter":
        # 数据存在才可以修改
        alter_vehicle = Vehicle.query.filter(Vehicle.ID == vehicle_number).first()
        vehicletype = VehicleType.query.filter(VehicleType.ID == vehicle_type).first()
        if alter_vehicle:
            alter_vehicle.Liscense = vehicle_liscence
            alter_vehicle.VehicleType = vehicletype
            alter_vehicle.color = vehicle_color
            alter_vehicle.FrameID = vehicle_frame_id
            alter_vehicle.Updater = operator
            alter_vehicle.UpdateTime = datetime.now()
            db.session.add(alter_vehicle)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_vehicle = Vehicle.query.filter_by(Liscense=vehicle_liscence).first()
        vehicletype = VehicleType.query.filter(VehicleType.ID == vehicle_type).first()
        # 数据没有重名的可以添加
        if not old_vehicle:
            old_vehicle = Vehicle(Liscense=vehicle_liscence)
            old_vehicle.color = vehicle_color
            old_vehicle.FrameID = vehicle_frame_id
            old_vehicle.VehicleType = vehicletype
            old_vehicle.Creater = operator
            old_vehicle.Updater = operator
            db.session.add(old_vehicle)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete_vehicle = Vehicle.query.filter(Vehicle.ID == vehicle_number).first()
        if delete_vehicle:
            db.session.delete(delete_vehicle)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询仓库数据
def query_warehouse(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    warehouse_name = json_data.get("WarehouseName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, warehouse_name, start_page, per_page, start_date, end_date)
    warehouse_name.strip()
    if len(warehouse_name) != 0:
        page_data = WareHouseType.query.filter(WareHouseType.Name == warehouse_name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = WareHouseType.query.filter(WareHouseType.CreateTime.between(start_date, end_date)) \
                    .order_by(WareHouseType.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = WareHouseType.query.order_by(WareHouseType.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for warehouse in page_data.items:
        if warehouse.Enabled:
            enable = "启用"
        else:
            enable = "停用"
        row = {
               "ID": warehouse.ID, "Name": warehouse.Name,  "Enabled": enable,
               "Creater": warehouse.Creater.Name, "Updater": warehouse.Updater.Name,
               "CreateTime": str(warehouse.CreateTime), "UpdateTime": str(warehouse.UpdateTime)
               }
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑仓库数据
def edit_warehouse(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    number = json_data.get("Number")
    name = json_data.get("WarehouseName")
    enabled = json_data.get("Enabled")
    operator = User.query.filter(User.Name == sender).first()
    if operation == "alter":
        # 数据存在才可以修改
        warehouse = WareHouseType.query.filter(WareHouseType.ID == number).first()
        if warehouse:
            warehouse.Name = name
            warehouse.Enabled = int(enabled)
            warehouse.Updater = operator
            warehouse.UpdateTime = datetime.now()
            db.session.add(warehouse)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_warehouse = WareHouseType.query.filter_by(Name=name).first()
        # 数据没有重名的可以添加
        if not old_warehouse:
            old_warehouse = WareHouseType(Name=name)
            old_warehouse.Enabled = int(enabled)
            old_warehouse.Creater = operator
            old_warehouse.Updater = operator
            db.session.add(old_warehouse)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete = WareHouseType.query.filter(WareHouseType.ID == number).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询银行类型
def query_banktype(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    name = json_data.get("BankTypeName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, name, start_page, per_page, start_date, end_date)
    name.strip()
    if len(name) != 0:
        page_data = BankType.query.filter(BankType.Name == name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = BankType.query.filter(BankType.CreateTime.between(start_date, end_date)) \
                    .order_by(BankType.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = BankType.query.order_by(BankType.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for banktype in page_data.items:
        row = {
               "ID": banktype.ID, "Name": banktype.Name,
               "Creater": banktype.Creater.Name, "Updater": banktype.Updater.Name,
               "CreateTime": str(banktype.CreateTime), "UpdateTime": str(banktype.UpdateTime)
               }
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑银行类型
def edit_banktype(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    number = json_data.get("Number")
    name = json_data.get("BankTypeName")
    operator = User.query.filter(User.Name == sender).first()
    if operation == "alter":
        # 数据存在才可以修改
        banktype = BankType.query.filter(BankType.ID == number).first()
        if banktype:
            banktype.Name = name
            banktype.Updater = operator
            banktype.UpdateTime = datetime.now()
            db.session.add(banktype)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        old_banktype = BankType.query.filter_by(Name=name).first()
        # 数据没有重名的可以添加
        if not old_banktype:
            old_banktype = BankType(Name=name)
            old_banktype.Creater = operator
            old_banktype.Updater = operator
            db.session.add(old_banktype)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete = BankType.query.filter(BankType.ID == number).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)


# 查询售粮户
def query_seller(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    name = json_data.get("SellerName")
    start_page = json_data.get("StartPage")
    per_page = json_data.get("PerPage")
    start_date = json_data.get("StartDate")
    end_date = json_data.get("EndDate")
    print(sender, name, start_page, per_page, start_date, end_date)
    name.strip()
    if len(name) != 0:
        page_data = Seller.query.filter(Seller.Name == name)\
                    .paginate(page=int(start_page), per_page=int(per_page))
    elif start_date and end_date is not None:
        page_data = Seller.query.filter(Seller.CreateTime.between(start_date, end_date)) \
                    .order_by(Seller.CreateTime.desc()) \
                    .paginate(page=int(start_page), per_page=int(per_page))
    else:
        page_data = Seller.query.order_by(Seller.CreateTime.desc())\
                    .paginate(page=int(start_page), per_page=int(per_page))

    query_list = list()
    print(page_data.total)
    print(page_data.pages)  # 当前查询的数据一共有多少页
    for seller in page_data.items:
        row = {
               "ID": seller.ID, "Name": seller.Name, "IdentityID": seller.IdentityID,  "Address": seller.Address,
               "Phone": seller.Phone, "BankType": seller.BankType.Name, "BankID": seller.BankID,
               "Creater": seller.Creater.Name, "Updater": seller.Updater.Name,
               "CreateTime": str(seller.CreateTime), "UpdateTime": str(seller.UpdateTime)
               }
        query_list.append(row)

    result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": start_page,
              "TotalData": page_data.total, "Data": query_list}
    return json.dumps(result)


# 编辑售粮户
def edit_seller(json_data):
    print(json_data)
    cmd = json_data.get("Cmd")
    sender = json_data.get("Sender")
    operation = json_data.get("Operation")
    number = json_data.get("Number")
    name = json_data.get("SellerName")
    identity = json_data.get("IdentityID")
    address = json_data.get("SellerAddress")
    phone = json_data.get("SellerPhone")
    bank_type = json_data.get("BankType")
    bank_id = json_data.get("BankId")
    operator = User.query.filter(User.Name == sender).first()

    banktype = BankType.query.filter(BankType.ID == bank_type).first()
    if operation == "alter":
        # 数据存在才可以修改
        seller = Seller.query.filter(Seller.ID == number).first()
        if seller:
            seller.Name = name
            seller.IdentityID = identity
            seller.Address = address
            seller.Phone = phone
            seller.BankType = banktype
            seller.id = bank_id
            seller.Updater = operator
            seller.UpdateTime = datetime.now()
            db.session.add(seller)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            result = {"Cmd": cmd, "Errno": 4, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
    elif operation == "add":
        new_seller = Seller.query.filter_by(Name=name).first()
        # 数据没有重名的可以添加
        if not new_seller:
            new_seller = Seller(Name=name)
            new_seller.IdentityID = identity
            new_seller.Address = address
            new_seller.Phone = phone
            new_seller.BankType = banktype
            new_seller.BankID = bank_id
            new_seller.Creater = operator
            new_seller.Updater = operator
            db.session.add(new_seller)
            db.session.commit()
            result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                      "TotalData": "", "Data": ""}
        else:
            # 数据重名了
            result = {"Cmd": cmd, "Errno": 3, "ErrMsg": "The modified data does not exist", "Page": "",
                      "TotalData": "", "Data": ""}
    if operation == "delete":
        # 先查询删除的数据是否存在
        delete = Seller.query.filter(Seller.ID == number).first()
        if delete:
            db.session.delete(delete)
            db.session.commit()
        result = {"Cmd": cmd, "Errno": 0, "ErrMsg": "noError", "Page": "",
                  "TotalData": "", "Data": ""}
    return json.dumps(result)

