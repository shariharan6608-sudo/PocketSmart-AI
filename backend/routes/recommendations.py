from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.database import get_db
from backend.models.user import User
from backend.models.recommendation import Recommendation
from backend.services.auth_dependency import get_current_user
from backend.services.gemini_service import generate_recommendation


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


class RecommendationRequest(BaseModel):
    category: str
    budget: str
    preferences: str


@router.post("/generate")
def generate_ai_recommendation(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if request.category != "Home Budget":
        raise HTTPException(
            status_code=400,
            detail="Only Home Budget planning is available."
        )

    prompt = f"""
You are PocketSmart AI, an AI-powered Home Budget Planning Assistant.

Create a practical interior budget plan based on the user's information.

USER INFORMATION
----------------
Total Budget:
{request.budget}

Home Details:
{request.preferences}

IMPORTANT INSTRUCTIONS
----------------------
1. Stay within the user's total budget.
2. Create a clear budget allocation.
3. Use realistic estimated amounts in Indian Rupees.
4. Cover the important home interior areas.
5. Do not recommend specific online stores or products.
6. Do not invent exact market prices.
7. Clearly mention that prices are estimates.
8. Keep the plan practical for a normal Indian home.
9. Include a small contingency amount if the budget allows.

RETURN THE RESULT IN THIS FORMAT
--------------------------------

🏠 HOME BUDGET PLAN

Total Budget:
₹X

1. Living Room
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

2. Bedroom
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

3. Kitchen
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

4. Lighting & Electrical
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

5. Furniture & Storage
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

6. Decor & Finishing
Estimated Budget: ₹X
Percentage: X%
Purpose: ...

7. Contingency
Estimated Budget: ₹X
Percentage: X%
Purpose: Unexpected expenses.

TOTAL ALLOCATED:
₹X

REMAINING:
₹X

💡 MONEY-SAVING TIPS
- ...
- ...
- ...

⚠️ NOTE
All amounts are approximate estimates. Actual costs can vary depending on materials, labour, location, size, and design choices.
"""

    recommendation_text = generate_recommendation(prompt)

    # Do not save failed AI responses into the database.
    if recommendation_text in [
        "AI_LIMIT_REACHED",
        "No recommendation was generated."
    ] or recommendation_text.startswith(
        "AI generation error:"
    ):

        return {
            "message": "AI recommendation could not be generated.",
            "recommendation": recommendation_text
        }

    new_recommendation = Recommendation(
        user_id=current_user.id,
        category=request.category,
        budget=request.budget,
        preferences=request.preferences,
        recommendation=recommendation_text,
        created_at=datetime.now(
            timezone.utc
        ).isoformat()
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return {
        "message": "Home budget plan generated successfully",
        "user": current_user.username,
        "recommendation_id": new_recommendation.id,
        "category": request.category,
        "budget": request.budget,
        "recommendation": recommendation_text
    }


@router.get("/latest-home")
def get_latest_home_recommendation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    recommendation = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id ==
            current_user.id
        )
        .filter(
            Recommendation.category ==
            "Home Budget"
        )
        .order_by(
            Recommendation.id.desc()
        )
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="No home budget plan found."
        )

    return {
        "id": recommendation.id,
        "category": recommendation.category,
        "budget": recommendation.budget,
        "preferences": recommendation.preferences,
        "recommendation": recommendation.recommendation,
        "created_at": recommendation.created_at
    }