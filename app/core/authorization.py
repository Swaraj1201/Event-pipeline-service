from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user


def require_role(required_role: str):
    """
    Dependency factory to enforce role-based access control.
    
    Args:
        required_role: The role required to access the endpoint
        
    Returns:
        Dependency function that checks if current user has the required role
        
    Raises:
        HTTPException: 403 if user doesn't have the required role
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        """
        Check if current user has the required role.
        
        Args:
            current_user: Current user context from JWT token
            
        Returns:
            dict: Current user context if authorized
            
        Raises:
            HTTPException: 403 Forbidden if user doesn't have required role
        """
        user_role = current_user.get("role")
        
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}",
            )
        
        return current_user
    
    return role_checker


def require_any_role(*allowed_roles: str):
    """
    Dependency factory to enforce role-based access control with multiple allowed roles.
    
    Args:
        *allowed_roles: Variable number of roles that are allowed to access the endpoint
        
    Returns:
        Dependency function that checks if current user has one of the allowed roles
        
    Raises:
        HTTPException: 403 if user doesn't have any of the required roles
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        """
        Check if current user has one of the allowed roles.
        
        Args:
            current_user: Current user context from JWT token
            
        Returns:
            dict: Current user context if authorized
            
        Raises:
            HTTPException: 403 Forbidden if user doesn't have any of the allowed roles
        """
        user_role = current_user.get("role")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}",
            )
        
        return current_user
    
    return role_checker
