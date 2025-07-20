from pydantic import BaseModel, Field

class HandoffData(BaseModel):
    agent_ip :str = Field(description= "6 topics from Assistant")
    user_input: str = Field(description="Input from User")