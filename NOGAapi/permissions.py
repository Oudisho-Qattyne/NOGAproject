from rest_framework.permissions import BasePermission

class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isCEO = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isCEO = bool(request.user.employee.job_type.job_type == 'CEO')
                return bool(request.user and request.user.is_authenticated and isCEO ) 
    

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isManager = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isManager = bool(request.user.employee.job_type.job_type == 'Manager')
                return bool(request.user and request.user.is_authenticated and isManager )
    
class IsHR(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isHR = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isHR = bool(request.user.employee.job_type.job_type == 'HR')
                return bool(request.user and request.user.is_authenticated and isHR )
    
class IsSalesOfficer(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isSalesOfficer= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isSalesOfficer = bool(request.user.employee.job_type.job_type == 'Sales Officer')
                return bool(request.user and request.user.is_authenticated and isSalesOfficer )

class IsSalesOfficerOrCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isSalesOfficerOrCEO= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isSalesOfficerOrCEO = bool(request.user.employee.job_type.job_type == 'Sales Officer' or request.user.employee.job_type.job_type == 'CEO')
                return bool(request.user and request.user.is_authenticated and isSalesOfficerOrCEO )


class IsHROrCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool(request.user and request.user.is_staff)):
            return True
        else:
            isHROrCEO= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isHROrCEO = bool(request.user.employee.job_type.job_type == 'CEO' or request.user.employee.job_type.job_type == 'HR')
                return bool(request.user and request.user.is_authenticated and isHROrCEO )

