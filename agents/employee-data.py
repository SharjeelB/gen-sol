import json

class JsonAgent:

    def __init__(self, json_file):
        with open(json_file, "r") as file:
            self.data = json.load(file)

    def get_employee_by_name(self, name):
        for emp in self.data["employees"]:
            if emp["name"].lower() == name.lower():
                return emp
        return None

    def get_department(self, name):
        employee = self.get_employee_by_name(name)
        if employee:
            return employee["department"]
        return "Employee not found"

    def get_salary(self, name):
        employee = self.get_employee_by_name(name)
        if employee:
            return employee["salary"]
        return "Employee not found"

    def list_employees(self):
        return [emp["name"] for emp in self.data["employees"]]

    def process_query(self, query):

        query = query.lower()

        if "list" in query:
            return self.list_employees()

        if "department" in query:
            for emp in self.data["employees"]:
                if emp["name"].lower() in query:
                    return self.get_department(emp["name"])

        if "salary" in query:
            for emp in self.data["employees"]:
                if emp["name"].lower() in query:
                    return self.get_salary(emp["name"])

        return "Sorry, I don't understand."


if __name__ == "__main__":

    agent = JsonAgent("data/employee.json")

    print("Simple JSON Agent")
    print("Examples:")
    print("- List employees")
    print("- What is John's salary?")
    print("- Which department does Alice work in?")
    print()

    while True:
        question = input("You: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = agent.process_query(question)
        print("Agent:", answer)