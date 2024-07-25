from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import *

SAFE_METHODS = ['GET']

class IsCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isCEO = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isCEO = bool(request.user.employee.job_type.job_type == 'CEO')
                return bool(request.user and request.user.is_authenticated and isCEO ) 
    

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isManager = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isManager = bool(request.user.employee.job_type.job_type == 'Manager')
                return bool(request.user and request.user.is_authenticated and isManager )
    
class IsHR(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isHR = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isHR = bool(request.user.employee.job_type.job_type == 'HR')
                return bool(request.user and request.user.is_authenticated and isHR )
            
class IsWarehouseAdministrator(BasePermission):
    def has_permission( self, request, view):
        if(bool(  request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isWarehouseAdministrator = False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isWarehouseAdministrator = bool(request.user.employee.job_type.job_type == 'Warehouse Administrator')
                return bool(request.user and request.user.is_authenticated and isWarehouseAdministrator )        
            
                
class PermissionOnEmployees(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            print("not admin")
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type') and request.user.employee.job_type.job_type == 'HR'):
                    print("in HR")
                    if('job_type' in request.data and request.data['job_type'] in [1 , 2 , 3]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")
                    else:
                        return True
                elif(hasattr(request.user.employee , 'job_type') and request.user.employee.job_type.job_type == 'CEO'):
                    print("in CEO")
                    if('job_type' in request.data and request.data['job_type'] not in [1 , 2 , 3]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")
                    else:
                        return True
                else:
                    return False
                
                
    def has_object_permission(self, request, view, obj):
        if(bool(  request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            print("not admin")
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type') and request.user.employee.job_type.job_type == 'HR'):
                    print("in HR")
                    if(hasattr(obj , 'job_type') and obj.job_type.job_type in ["HR" , "CEO" , "Warehouse Administrator"]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")            

                    elif('job_type' in request.data and request.data['job_type'] in [1 , 2 , 3]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")            

                    # elif(hasattr(obj , 'job_type') and obj.job_type.job_type=='Manager'):
                    #     print(obj.id)
                    #     branches = Branch.objects.all()
                    #     relatedBranches = branches.filter(manager= obj.id)
                    #     if(len(relatedBranches) > 0 ):
                    #         # self.message = 
                    #         raise PermissionDenied("this employee is a manager to a branche , change the manager on this branch then edit this employee")            
                    #     else:
                    #         return True
                    else:
                        return True
                elif(hasattr(request.user.employee , 'job_type') and request.user.employee.job_type.job_type == 'CEO'):
                    print("in CEO")
                    if(hasattr(obj , 'job_type') and obj.job_type.job_type  not in ["HR" , "CEO" , "Warehouse Administrator"]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")
                    elif('job_type' in request.data and request.data['job_type'] not in [1 , 2 , 3]):
                        raise PermissionDenied("You do not have permission to add/update employee with this job type")
                    else:
                        return True
                else:
                    return False
    
    
    
class IsSalesOfficer(BasePermission):
    def has_permission(self, request, view):
        if(bool(  request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isSalesOfficer= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isSalesOfficer = bool(request.user.employee.job_type.job_type == 'Sales Officer')
                return bool(request.user and request.user.is_authenticated and isSalesOfficer )

class IsSalesOfficerOrCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isSalesOfficerOrCEO= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isSalesOfficerOrCEO = bool(request.user.employee.job_type.job_type == 'Sales Officer' or request.user.employee.job_type.job_type == 'CEO')
                return bool(request.user and request.user.is_authenticated and isSalesOfficerOrCEO )


class IsHROrCEO(BasePermission):
    def has_permission(self, request, view):
        if(bool( request.method in SAFE_METHODS or request.user and request.user.is_staff)):
            return True
        else:
            isHROrCEO= False
            if( request.user and hasattr(request.user, 'employee')):
                if(hasattr(request.user.employee , 'job_type')):
                    isHROrCEO = bool(request.user.employee.job_type.job_type == 'CEO' or request.user.employee.job_type.job_type == 'HR')
                return bool(request.user and request.user.is_authenticated and isHROrCEO )

