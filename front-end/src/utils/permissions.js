import { UserModule } from "../store";

export function hasPermission(permissions) {
  const { permissions: userPermissions, isSuperuser } = UserModule;

  if (!isSuperuser && permissions?.length) {
    return permissions.some(permission => {
      if (typeof permission === "string") {
        return userPermissions?.find(
          userPermission => userPermission.codename === permission,
        );
      }
      if (typeof permission === "object") {
        return userPermissions?.find(
          userPermission => userPermission.codename === permission.codename
            && permission.validator(),
        );
      }
      return false;
    });
  }
  return true;
}

export function getDisciplinePersonsFilters(entity, method) {
  const {
    personMilfaculty, personMilgroup, personType, personId,
  } = UserModule;

  const students = {
    milfaculty: personMilfaculty,
  };

  if (hasPermission([`${entity}.${method}.all`])) {
    return {};
  }
  if (hasPermission([`${entity}.${method}.milfaculty`])) {
    return {
      students,
      teachers: {
        milfaculty: personMilfaculty,
      },
    };
  }
  if (hasPermission([`${entity}.${method}.milgroup`])) {
    if (personType === "student") {
      return {
        students,
        teachers: {
          milgroup: personMilgroup,
        },
      };
    }
    if (personType === "teacher") {
      return {
        students,
        teachers: {
          id: personId,
        },
      };
    }
  }
  if (hasPermission([`${entity}.${method}.self`])) {
    if (personType === "student") {
      return {
        students: {
          id: personId,
        },
      };
    }
    if (personType === "teacher") {
      return {
        students,
        teachers: {
          id: personId,
        },
      };
    }
  }
  return {};
}
