
from fastapi import Header, HTTPException

from app.database import get_user_client, SUPABASE_URL, SUPABASE_KEY
from supabase import create_client


def get_current_user(authorization: str = Header(None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication token is required"
        )

    token = authorization.split(" ", 1)[1]

    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)

        # Verify the user's access token.
        auth_response = client.auth.get_user(token)
        auth_user = auth_response.user

        if auth_user is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Use a separate client carrying this user's token.
        user_client = get_user_client(token)

        profile_response = (
            user_client.table("users")
            .select("id, company_id, role, full_name")
            .eq("id", str(auth_user.id))
            .execute()
        )

        if not profile_response.data:
            raise HTTPException(
                status_code=403,
                detail="User profile not found"
            )

        profile = profile_response.data[0]

        return {
            "id": str(auth_user.id),
            "company_id": profile["company_id"],
            "role": profile["role"],
            "supabase": user_client
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )
