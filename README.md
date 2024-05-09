
---

# Vendor Management System with Performance Metrics

This project is a Vendor Management System built using Django and Django REST Framework. It allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/AbdullajonOdilov/vms.git
   ```

2. Navigate to the project directory:
   ```bash
   cd vms
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations to create the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the admin panel at `http://127.0.0.1:8000/admin/` to manage vendors, purchase orders, and historical performance records.

## API Endpoints

- **Vendors API**:
  - `POST /api/vendors/`: Create a new vendor.
  - `GET /api/vendors/`: List all vendors.
  - `GET /api/vendors/{vendor_id}/`: Retrieve details of a specific vendor.
  - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
  - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

- **Purchase Orders API**:
  - `POST /api/purchase_orders/`: Create a new purchase order.
  - `GET /api/purchase_orders/`: List all purchase orders.
  - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
  - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
  - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.
  - `POST /api/purchase_orders/{po_id}/acknowledge`: Acknowledge a purchase order.

- **Vendor Performance API**:
  - `GET /api/vendors/{vendor_id}/performance`: Retrieve performance metrics for a specific vendor.

## Running the Test Suite

1. Ensure the development server is running.

2. Open a new terminal and navigate to the project directory.

3. Run the test suite using the following command:
   ```bash
   python manage.py test
   ```

4. View the test results and ensure all tests pass successfully.

## Additional Notes

- For comprehensive API documentation, access the built-in DRF documentation at `http://127.0.0.1:8000/` after running the development server.

- Make sure to handle data validations, error responses, and implement real-time updates for performance metrics as per the technical requirements.

---
