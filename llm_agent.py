import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool, StructuredTool
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel
from database import get_available_appointments, book_appointment, list_doctors

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class BookDoctorInput(BaseModel):
    name: str
    doctor: str
    department: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM (24-hour)

# Define helper functions
def get_doctors_by_issue(issue):
    issue = issue.lower()
    
    # Gastroenterology
    if "stomach" in issue or "abdomen" in issue or "digestion" in issue or "constipation" in issue:
        return "Dr. Mehta (Gastroenterology)"
    
    # Cardiology
    elif "heart" in issue or "chest pain" in issue:
        return "Dr. Taylor (Cardiology)"
    
    # Dermatology
    elif "skin" in issue or "rash" in issue or "acne" in issue:
        return "Dr. Smith (Dermatology)"
    
    # Pediatrics
    elif "child" in issue or "fever" in issue or "cough" in issue:
        return "Dr. Patel (Pediatrics)"
    
    # Orthopedics
    elif "pain" in issue or "bone" in issue or "joint" in issue or "back" in issue:
        return "Dr. Johnson (Orthopedics)"
    
    # Neurology
    elif "headache" in issue or "migraine" in issue or "brain" in issue or "numbness" in issue:
        return "Dr. Chen (Neurology)"
    
    return "Sorry, I need more details to recommend the right doctor."


def fetch_slots_for_doctor(doctor_name):
    slots = get_available_appointments()
    available = [s for s in slots if s.DoctorName == doctor_name]
    if not available:
        return "No available slots found."
    return "\n".join([f"{s.AppointmentDate} at {s.AppointmentTime}" for s in available])

def book_slot(name, doctor, department, date, time):
    return book_appointment(name, doctor, department, date, time)

# Define tools
from langchain.tools import Tool, StructuredTool

# Define tools
tools = [
    Tool(
        name="GetDoctorByIssue",
        func=get_doctors_by_issue,
        description="Suggest a doctor based on user's symptoms."
    ),
    Tool(
        name="FetchDoctorSlots",
        func=fetch_slots_for_doctor,
        description="List available slots for a specific doctor."
    ),
    StructuredTool(  # ✅ use this for multi-argument schema input
        name="BookDoctorAppointment",
        func=book_slot,
        args_schema=BookDoctorInput,
        description="Book an appointment with a doctor. Requires name, doctor, department, date, and time."
    ),
    Tool(
        name="ListAvailableDoctors",
        func=list_doctors,
        description="Returns a list of all doctors and their departments."
    )
]


# Create LLM
llm = ChatOpenAI(temperature=0)

# Define memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Build prompt manually (new LangChain 0.1+ way)
prompt = ChatPromptTemplate.from_messages([
   ("system", "You are a helpful assistant that books doctor appointments. "
    "Always ask for the patient's full name before confirming any booking. "
    "Use that name when submitting the booking request."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # <-- required
])

# Create agent + executor
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# Chat loop
print("🤖 Hello! I can help you book doctor appointments. Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Goodbye!")
        break
    result = agent_executor.invoke({"input": user_input})
    print("\nAssistant:", result["output"])
