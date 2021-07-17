import { UserModule } from "../store";

export function hasPermission(permissions) {
  const userPermissions = UserModule.permissions;

  if (permissions?.length) {
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
