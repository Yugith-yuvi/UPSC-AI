import os
import random
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, JSON, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional, Dict

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./upsc_prep.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    year = Column(Integer, index=True)
    exam_type = Column(String, default="Prelims")
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    is_premium = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


class QuestionSchema(BaseModel):
    id: int
    subject: str
    year: int
    exam_type: str
    question: str
    options: Dict[str, str]
    correct_option: str
    explanation: Optional[str] = None
    is_premium: bool

    class Config:
        from_attributes = True


app = FastAPI(title="UPSC Prep Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_initial_data():
    db = SessionLocal()
    # Create the table when needed. Do not delete the user's saved questions.
    Base.metadata.create_all(bind=engine)

    dataset = [
        # POLITY
        QuestionModel(
            subject="Polity & Governance", year=2023, exam_type="Prelims",
            question="Which one of the following statements best reflects the chief purpose of the 'Constitution of India'?",
            options={"A": "Determines lawmaking objectives.", "B": "Creates political offices.", "C": "Defines and limits the powers of government.", "D": "Secures social justice."},
            correct_option="C", explanation="Constitutionalism defines and limits government authority to protect fundamental rights.", is_premium=False
        ),
        QuestionModel(
            subject="Polity & Governance", year=2021, exam_type="Prelims",
            question="Which one of the following in Indian polity is an essential feature that indicates that it is federal in character?",
            options={"A": "The independence of judiciary is safeguarded.", "B": "The Union Legislature has elected representatives.", "C": "The Union Cabinet can have regional members.", "D": "Fundamental Rights are enforceable."},
            correct_option="A", explanation="An independent judiciary safeguards the constitutional distribution of powers.", is_premium=False
        ),
        QuestionModel(
            subject="Polity & Governance", year=2020, exam_type="Prelims",
            question="A Parliamentary System of Government is one in which:",
            options={"A": "All political parties are represented.", "B": "Government is responsible to Parliament and removable by it.", "C": "Government is elected by the people directly.", "D": "Fixed term for government."},
            correct_option="B", explanation="The Executive is directly accountable to the Legislature in a Parliamentary system.", is_premium=False
        ),

        # ECONOMY
        QuestionModel(
            subject="Economy", year=2022, exam_type="Prelims",
            question="With reference to Indian economy, consider Inflation-Indexed Bonds (IIBs):\n1. Govt can reduce coupon rates.\n2. IIBs protect investors from inflation.\nWhich statement is correct?",
            options={"A": "1 only", "B": "2 only", "C": "Both 1 and 2", "D": "Neither 1 nor 2"},
            correct_option="C", explanation="IIBs protect principal against inflation and reduce real borrowing costs for the government.", is_premium=False
        ),
        QuestionModel(
            subject="Economy", year=2021, exam_type="Prelims",
            question="If RBI adopts an 'Expansionary Monetary Policy', which of the following would it NOT do?",
            options={"A": "Cut SLR", "B": "Increase MSF Rate", "C": "Cut Repo Rate", "D": "Cut Bank Rate"},
            correct_option="B", explanation="Increasing MSF rate restricts liquidity (contractionary policy).", is_premium=False
        ),
        QuestionModel(
            subject="Economy", year=2020, exam_type="Prelims",
            question="Which of the following describes the term 'Money Multiplier'?",
            options={"A": "Ratio of currency with public to aggregate deposits", "B": "Ratio of bank deposits to reserve money", "C": "Increase in Banking Habit of population", "D": "Ratio of total money supply to population"},
            correct_option="C", explanation="Banking habits increase credit creation, expanding money multiplier.", is_premium=False
        ),

        # MODERN HISTORY
        QuestionModel(
            subject="Modern History", year=2021, exam_type="Prelims",
            question="With reference to Indian history, 'Ulgulan' or the Great Tumult describes which event?",
            options={"A": "The Revolt of 1857", "B": "The Mappila Rebellion of 1921", "C": "The Indigo Revolt of 1859-60", "D": "Birsa Munda's Revolt of 1899-1900"},
            correct_option="D", explanation="Birsa Munda led the Ulgulan rebellion against land alienation.", is_premium=False
        ),
        QuestionModel(
            subject="Modern History", year=2020, exam_type="Prelims",
            question="With reference to Indigo cultivation in India, why did it decline in the early 20th century?",
            options={"A": "Peasant resistance", "B": "Unprofitability due to synthetic dyes", "C": "Nationalist opposition", "D": "Government control"},
            correct_option="B", explanation="German synthetic dyes made natural indigo commercially unviable.", is_premium=False
        ),

        # ENVIRONMENT & ECOLOGY
        QuestionModel(
            subject="Environment & Ecology", year=2022, exam_type="Prelims",
            question="Which one of the following is a filter feeder?",
            options={"A": "Catfish", "B": "Oyster", "C": "Octopus", "D": "Pelican"},
            correct_option="B", explanation="Oysters filter water to feed on plankton and organic matter.", is_premium=False
        ),
        QuestionModel(
            subject="Environment & Ecology", year=2021, exam_type="Prelims",
            question="Which of the following are nitrogen-fixing plants?\n1. Chickpea\n2. Clover\n3. Purslane\n4. Spinach\n5. Vetch",
            options={"A": "1, 2 and 5 only", "B": "1, 3 and 4 only", "C": "2, 4 and 5 only", "D": "1, 2, 3, 4 and 5"},
            correct_option="A", explanation="Legumes like Chickpea, Clover, and Vetch host nitrogen-fixing bacteria.", is_premium=False
        ),

        # SCIENCE & TECHNOLOGY
        QuestionModel(
            subject="Science & Technology", year=2022, exam_type="Prelims",
            question="With reference to Web 3.0, consider:\n1. Enables users to control their own data.\n2. Can have blockchain-based social networks.",
            options={"A": "1 only", "B": "2 only", "C": "Both 1 and 2", "D": "Neither 1 nor 2"},
            correct_option="C", explanation="Web 3.0 focuses on decentralization and user data ownership.", is_premium=False
        ),

        # GEOGRAPHY
        QuestionModel(
            subject="Geography", year=2021, exam_type="Prelims",
            question="Which of the following rivers rise from the Eastern Ghats?\n1. Brahmani\n2. Nagavali\n3. Subarnarekha\n4. Vamsadhara",
            options={"A": "1 and 2", "B": "2 and 4", "C": "3 and 4", "D": "1 and 3"},
            correct_option="B", explanation="Nagavali and Vamsadhara originate in the Eastern Ghats.", is_premium=False
        )
    ]

    # Add new seed records without duplicating rows or deleting saved questions.
    existing = db.query(QuestionModel).all()
    existing_keys = {
        (item.subject, item.year, item.exam_type, item.question)
        for item in existing
    }
    db.add_all([
        item for item in dataset
        if (item.subject, item.year, item.exam_type, item.question) not in existing_keys
    ])
    db.commit()
    db.close()


@app.get("/api/v1/pyq/fetch", response_model=Dict[str, List[QuestionSchema]])
def fetch_questions(
    subject: str = Query(...),
    year: Optional[int] = Query(None, description="Exact year requested"),
    year_start: Optional[int] = Query(None, ge=2000, le=2100),
    year_end: Optional[int] = Query(None, ge=2000, le=2100),
    exam_type: str = Query("Prelims"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Always apply every selected filter. Never substitute unrelated questions.
    query = db.query(QuestionModel).filter(
        QuestionModel.subject == subject,
        QuestionModel.exam_type == exam_type
    )

    if year:
        query = query.filter(QuestionModel.year == year)
    if year_start is not None:
        query = query.filter(QuestionModel.year >= year_start)
    if year_end is not None:
        query = query.filter(QuestionModel.year <= year_end)
    if year_start is not None and year_end is not None and year_start > year_end:
        return {"data": []}

    questions = query.order_by(QuestionModel.year.desc()).all()

    sample_size = min(len(questions), limit)
    selected = random.sample(questions, sample_size) if sample_size else []
    random.shuffle(selected)

    return {"data": selected}
