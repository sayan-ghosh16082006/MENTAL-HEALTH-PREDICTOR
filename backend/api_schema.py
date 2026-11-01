from pydantic import BaseModel, Field
from typing import Annotated, Literal



class InputData(BaseModel):

    Age                         : Annotated[int, Field(..., ge=10, le=100, description="The age of the student")]
    Gender                      : Annotated[Literal["Male", "Female"], Field(...)]
    Country                     : Annotated[Literal['India', 'USA', 'Canada', 'Australia', 'UK', 'Germany','Mexico', 'Turkey', 'France', 'Spain', 'Ireland', 'Japan', 'Denmark','Switzerland', 'Nepal', 'Italy', 'Russia', 'Sri Lanka', 'Maldives', 'Other'], Field(..., description="Country of student")]
    Academic_Level              : Annotated[Literal['Undergraduate', 'Graduate', 'High School'], Field(..., description="Academic Level of student")]
    Most_Used_Platform          : Annotated[Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter', 'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp', 'WeChat'], Field(..., description="The most used platform used by the student")]
    Purpose_Of_Use              : Annotated[Literal['Networking', 'Education', 'Entertainment', 'News'], Field(..., description="The pusrpose of use")]
    Avg_Daily_Usage_Hours       : Annotated[float, Field(..., ge = 0, le = 24,description="The avg daily usage")]
    Daily_Unlocks               : Annotated[int, Field(..., ge = 0,description="The daily number of unlocks")]
    Study_Hours                 : Annotated[float, Field(..., ge = 0, le = 24, description="The total study hours per day")]
    Physical_Activity_Hours     : Annotated[float, Field(..., ge = 0, le = 24, description="Physical Activity engagement time")]
    Sleep_Hours_Per_Night       : Annotated[float, Field(...,ge = 0, le = 24, description="Sleep hours per night of the student")]
    Stress_Level                : Annotated[Literal['Low', 'Medium', 'High', 'Very High'], Field(..., description="Stress Level of the student")]


class PredictedResponse(BaseModel):
    Mental_Health_Score : Annotated[float, Field(..., description="The Mental Health Score Of The Student")]





