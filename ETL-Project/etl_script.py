import csv
import json
import xml.etree.ElementTree as ET
import os
import logging
from dotenv import load_dotenv
from pony.orm import Database, Required, Optional, PrimaryKey, db_session, commit, LongStr
import pymysql

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load environment variables
load_dotenv()

# File paths
FILE_PATHS = {
    "customers_csv": r"ETL-Project\customers.csv",
    "customers_json": r"ETL-Project\customers_subscriptions.json",
    "customers_billing": r"ETL-Project\customers_billing.xml",
    "employee_csv": r"ETL-Project\employees.csv",
    "employees_vehicles": r"ETL-Project\employees_vehicles.xml",
    "employees_salaries": r"ETL-Project\employees_salaries.json",
    "flagged_prompts": r"ETL-Project\flagged_prompts.txt"
}

# Setup DB
db = Database()

class Customer(db.Entity):
    id = PrimaryKey(int, auto=True)
    first_name = Optional(str)
    last_name = Optional(str)
    customer_type = Optional(str)
    email = Optional(str, unique=False)
    subscription_type = Optional(str)
    company_name = Optional(str)
    phone_number = Optional(str, default="")
    dob = Optional(str)
    sex = Optional(str)
    payment_method = Optional(str)
    street = Optional(str)
    city = Optional(str, nullable=True)
    postcode = Optional(str)
    card_number = Optional(str, nullable=True)
    card_cvv = Optional(str, nullable=True)
    name = Required(str)

class Employee(db.Entity):
    employee_id = PrimaryKey(str)
    first_name = Optional(str)
    last_name = Optional(str)
    role = Optional(str)
    department = Optional(str)
    age = Optional(int)
    retired = Optional(bool)
    dependants = Optional(int)
    marital_status = Optional(str)
    vehicle_registration = Optional(str)
    vehicle_make = Optional(str)
    vehicle_model = Optional(str)
    vehicle_year = Optional(int)
    salary = Optional(float)
    pension = Optional(float)
    commute_distance = Optional(float)
    flagged_prompts = Optional(LongStr)

# Bind DB
pymysql.install_as_MySQLdb()
try:
    db.bind(
        provider='mysql',
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    db.generate_mapping(create_tables=True)
    logging.info("DB binding successful.")
except Exception as e:
    logging.error(f"DB binding error: {e}")
    exit(1)

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
# Extract data from various file types
def extract_file(file_path, file_type="csv"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_type == "csv":
                return list(csv.DictReader(f))
            elif file_type == "json":
                return json.load(f)
            elif file_type == "xml":
                return ET.parse(f).getroot()
            elif file_type == "txt":
                return f.readlines()
    except FileNotFoundError:
        logging.warning(f"Missing file: {file_path}")
        return None if file_type == "xml" else []

def extract_customers_csv(path): return extract_file(path, "csv") or []
def extract_customers_json(path): return extract_file(path, "json") or []
def extract_file_json(path): return extract_file(path, "json") or []

def extract_customers_billing(path):
    root = extract_file(path, "xml")
    if root is None: return []
    billing = []
    for cust in root.findall('Customer'):
        name = f"{cust.findtext('FirstName', '')} {cust.findtext('LastName', '')}".strip() or cust.findtext('CompanyName', '')
        billing.append({
            'name': name,
            'phone_number': cust.findtext('PhoneNo', ''),
            'payment_method': cust.findtext('PaymentMethod', ''),
            'street': cust.findtext('BillingAddress/Street', ''),
            'city': cust.findtext('BillingAddress/City', ''),
            'postcode': cust.findtext('BillingAddress/Postcode', ''),
            'card_number': cust.findtext('CardDetails/CardNumber', ''),
            'card_cvv': cust.findtext('CardDetails/CVV', '')
        })
    return billing

def extract_vehicles(file_path):
    """Extract vehicle data from XML."""
    root = extract_file(file_path, file_type="xml")
    if not root:
        print("Failed to parse XML file or file is empty.")
        return []

    vehicle_data = []
    for employee in root.findall('Employee'):
        first_name = employee.get('FirstName', 'Unknown')
        last_name = employee.get('SecondName', 'Unknown')
        full_name = f"{first_name} {last_name}"

        vehicle_info = employee.find('VehicleInfo')
        if vehicle_info is not None:
            vehicle_data.append({
                'FullName': full_name,
                'RegistrationNumber': vehicle_info.findtext('RegistrationNumber'),
                'Make': vehicle_info.findtext('Make'),
                'Model': vehicle_info.findtext('Model'),
                'Year': safe_int(vehicle_info.findtext('Year'))
            })
    return vehicle_data


def extract_flagged_prompts(path):
    lines = extract_file(path, "txt") or []
    prompts, by_id = [], {}
    current_id = None
    for line in lines:
        line = line.strip()
        if line.startswith("Employee ID:"):
            current_id = line.split(":", 1)[1].strip()
            by_id.setdefault(current_id, [])
        elif line.startswith("Timestamp:") and current_id:
            by_id[current_id].append({'timestamp': line.split(":", 1)[1].strip(), 'prompt': ''})
        elif line.startswith("Prompt:") and current_id:
            by_id[current_id][-1]['prompt'] = line.split(":", 1)[1].strip()
    for eid, items in by_id.items():
        for p in items:
            prompts.append({'employee_id': eid, **p})
    return prompts

# Transform data into a unified format
def transform_customers(csv_data, json_data):
    customers = {}
    for c in csv_data + json_data:
        name = f"{c.get('first_name', '')} {c.get('last_name', '')}".strip() or c.get('company_name', '')
        if not name: continue
        key = name.strip()
        customers.setdefault(key, {
            'name': key,
            'first_name': c.get('first_name', ''),
            'last_name': c.get('last_name', ''),
            'company_name': c.get('company_name', ''),
            'customer_type': c.get('customer_type', ''),
            'subscription_type': c.get('subscription_type', ''),
            'email': c.get('email'),
            'phone_number': c.get('phone_number', ''),
            'dob': c.get('dob', ''),
            'sex': c.get('sex', '')
        }).update(c)
    return list(customers.values())

def transform_customers_with_billing(basic, billing):
    billing_map = {b['name']: b for b in billing}
    for cust in basic:
        b = billing_map.get(cust['name'], {})
        cust.update({
            'phone_number': cust.get('phone_number') or b.get('phone_number', ''),
            'payment_method': b.get('payment_method', ''),
            'street': b.get('street', ''),
            'city': b.get('city', ''),
            'postcode': b.get('postcode', ''),
            'card_number': b.get('card_number', ''),
            'card_cvv': b.get('card_cvv', '')
        })
    return basic

def transform_employees(employee_csv, vehicle_data, salary_data):
    """Transform employee data by merging with vehicle and salary information."""
    vehicle_dict = {v['FullName']: v for v in vehicle_data} if vehicle_data else {}
    salary_dict = {str(s['employee_id']): s for s in salary_data} if salary_data else {}

    unified_employees = []
    for emp in employee_csv:
        employee_id = emp.get('employee_id', '')
        if not employee_id:
            print(f"Skipping employee with missing ID: {emp}")
            continue

        first = emp.get('first_name', 'Unknown')
        last = emp.get('last_name', 'Unknown')
        full_name = f"{first} {last}"

        employee_info = {
            'employee_id': employee_id,
            'first_name': first,
            'last_name': last,
            'role': emp.get('role', 'Unknown'),
            'department': emp.get('department', 'Unknown'),
            'age': safe_int(emp.get('age')),
            'retired': emp.get('retired', 'false').lower() == 'true',
            'dependants': safe_int(emp.get('dependants', 0)),
            'marital_status': emp.get('marital_status', '')
        }

        # Merge vehicle data
        vehicle_info = vehicle_dict.get(full_name, {})
        employee_info.update({
            'vehicle_registration': vehicle_info.get('RegistrationNumber', ""),
            'vehicle_make': vehicle_info.get('Make', ""),
            'vehicle_model': vehicle_info.get('Model', ""),
            'vehicle_year': vehicle_info.get('Year', 0)
        })

        # Merge salary data
        salary_info = salary_dict.get(employee_id, {})
        employee_info.update({
            'salary': salary_info.get('salary', 0),
            'pension': salary_info.get('pension', 0),
            'commute_distance': salary_info.get('commute_distance', 0)
        })

        unified_employees.append(employee_info)

    return unified_employees

def merge_flagged_prompts(employees, prompts):
    by_id = {}
    for p in prompts:
        by_id.setdefault(p['employee_id'], []).append(p)
    for emp in employees:
        emp['flagged_prompts'] = json.dumps(by_id.get(emp['employee_id'], []))
    return employees

# Load data into the database
@db_session
def load_customers(customers):
    loaded, updated = 0, 0
    for c in customers:
        if not c.get('name'): continue
        existing = Customer.get(email=c.get('email')) if c.get('email') else None
        if existing:
            existing.set(**c)
            updated += 1
        else:
            Customer(**c)
            loaded += 1
    commit()
    logging.info(f"Customers: {loaded} added, {updated} updated.")

@db_session
def load_employees(employees):
    loaded, updated = 0, 0
    for e in employees:
        if not e.get('employee_id'): continue
        existing = Employee.get(employee_id=e['employee_id'])
        if existing:
            for key, val in e.items():
                setattr(existing, key, val)
            updated += 1
        else:
            Employee(**e)
            loaded += 1
    commit()
    logging.info(f"Employees: {loaded} added, {updated} updated.")

# Main ETL function
def run_etl():
    logging.info("Starting ETL process")
    c_csv = extract_customers_csv(FILE_PATHS["customers_csv"])
    c_json = extract_customers_json(FILE_PATHS["customers_json"])
    c_bill = extract_customers_billing(FILE_PATHS["customers_billing"])
    e_csv = extract_file(FILE_PATHS["employee_csv"], "csv") or []
    e_veh = extract_vehicles(FILE_PATHS["employees_vehicles"])
    e_sal = extract_file_json(FILE_PATHS["employees_salaries"])
    e_flags = extract_flagged_prompts(FILE_PATHS["flagged_prompts"])

    customers = transform_customers_with_billing(transform_customers(c_csv, c_json), c_bill)
    employees = merge_flagged_prompts(transform_employees(e_csv, e_veh, e_sal), e_flags)

    logging.info("Loading data to DB...")
    load_customers(customers)
    load_employees(employees)
    logging.info("ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()
