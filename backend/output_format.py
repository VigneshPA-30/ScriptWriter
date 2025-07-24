from pydantic import BaseModel, Field
from typing import List


class SearchOuputFormat(BaseModel):
    "All context from search result "
    search_report:str  =  Field(...,description="Report of all context from the search result relevant to the niche as mentioned in System Instructions")

class ResearchOutputFormat(BaseModel):
    topic:str = Field(...,description = "Topic selected after analysis")
    reason:str = Field(...,description="Reason for selection of this topic")


class ResearchOutputList(BaseModel):
    "List of research_output each with topic and reason. List should have 6 items no more no less"
    research_list:List[ResearchOutputFormat] = Field(...,description="List of research_output each with topic and reason. List should have 6 items no more no less")