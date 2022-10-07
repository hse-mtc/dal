import { UserModule } from "../store";

function permissionsLE(firstPermission, secondPermission) {
  const scopes = {
    all: 0,
    milfaculty: 10,
    milgroup: 20,
    self: 30,
  };
  // checks if pA < pB
  const firstPermissionSplit = firstPermission.split(".");
  const nameFirstPermission = firstPermissionSplit[0];
  const methodFirstPermission = firstPermissionSplit[1];
  const scopeFirstPermission = firstPermissionSplit[2];

  const secondPermissionSplit = secondPermission.split(".");
  const nameSecondPermission = secondPermissionSplit[0];
  const methodSecondPermission = secondPermissionSplit[1];
  const scopeSecondPermission = secondPermissionSplit[2];
  return (nameSecondPermission === nameFirstPermission)
  && (methodSecondPermission === methodFirstPermission)
  && (scopes[scopeFirstPermission] >= scopes[scopeSecondPermission]);
}

export function hasPermission(permissions) {
  const { permissions: userPermissions, isSuperuser } = UserModule;
  if (!isSuperuser && permissions?.length) {
    return permissions.some(permission => {
      if (typeof permission === "string") {
        return userPermissions?.find(
          userPermission => permissionsLE(permission, userPermission.codename),
        ); // userPermission.codename === permission
      }
      if (typeof permission === "object") {
        return userPermissions?.find(
          userPermission => permissionsLE(permission.codename, userPermission.codename)
          && permission.validator(),
        );// userPermission.codename === permission.codename
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
