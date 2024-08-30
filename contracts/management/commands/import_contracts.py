import openpyxl
from django.core.management.base import BaseCommand
from django.db import transaction
from contracts.models import Contract
from clients.models import Client
from utilities.models import Supplier, Utility
from django.db.models import Max
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime
import csv


class Command(BaseCommand):
    help = "Import data from Excel file with unique ID handling and foreign key relationships"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the Excel file")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        error_log_path = "import_errors.csv"

        import_order = [
            "id",
            "contract_type",
            "seamless_updated",
            "contract_status",
            "dwellent_id",
            "bid_id",
            "portal_status",
            "client",
            "client_group",
            "seed_stock",
            "client_manager",
            "is_directors_approval",
            "directors_approval_date",
            "business_name",
            "company_reg_number",
            "utility",
            "top_line",
            "mpan_mpr",
            "meter_serial_number",
            "meter_onboarded",
            "meter_status",
            "building_name",
            "site_address",
            "billing_address",
            "supplier",
            "supplier_coding",
            "contract_start_date",
            "contract_end_date",
            "lock_in_date",
            "supplier_start_date",
            "account_number",
            "eac",
            "day_consumption",
            "night_consumption",
            "vat_rate",
            "contract_value",
            "standing_charge",
            "sc_frequency",
            "unit_rate_1",
            "unit_rate_2",
            "unit_rate_3",
            "feed_in_tariff",
            "seamless_status",
            "profile",
            "is_ooc",
            "service_type",
            "pence_per_kilowatt",
            "day_kilowatt_hour_rate",
            "night_rate",
            "annualised_budget",
            "commission_per_annum",
            "commission_per_unit",
            "commission_per_contract",
            "partner_commission",
            "smart_meter",
            "vat_declaration_sent",
            "vat_declaration_date",
            "vat_declaration_expires",
            "notes",
            "kva",
            "future_supplier",
            "future_contract_start_date",
            "future_contract_end_date",
            "future_unit_rate_1",
            "future_unit_rate_2",
            "future_unit_rate_3",
            "future_standing_charge",
        ]

        date_fields = [
            "directors_approval_date",
            "contract_start_date",
            "contract_end_date",
            "lock_in_date",
            "supplier_start_date",
            "vat_declaration_date",
            "vat_declaration_expires",
            "future_contract_start_date",
            "future_contract_end_date",
            "meter_onboarded",
        ]

        decimal_fields = {
            "eac": 2,
            "contract_value": 2,
            "standing_charge": 4,
            "unit_rate_1": 6,
            "unit_rate_2": 6,
            "unit_rate_3": 6,
            "feed_in_tariff": 4,
            "commission_per_unit": 3,
            "future_unit_rate_1": 6,
            "future_unit_rate_2": 6,
            "future_unit_rate_3": 6,
            "future_standing_charge": 4,
        }

        def convert_date(date_string):
            if date_string and isinstance(date_string, str):
                try:
                    # Try parsing DD/MM/YYYY format
                    return datetime.strptime(date_string, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        # Try parsing DD-MM-YYYY format
                        return datetime.strptime(date_string, "%d-%m-%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Invalid date format: {date_string}. Keeping original value."
                            )
                        )
                        return date_string
            return date_string

        def convert_decimal(decimal_value, places):
            if decimal_value is not None and decimal_value != "":
                try:
                    return Decimal(decimal_value).quantize(
                        Decimal(f'0.{"0" * places}'), rounding=ROUND_HALF_UP
                    )
                except InvalidOperation:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Invalid decimal value: {decimal_value}. Keeping original value."
                        )
                    )
                    return decimal_value
            return decimal_value

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Get the maximum ID currently in the database
            max_id = Contract.objects.aggregate(Max("id"))["id__max"] or 0

            error_records = []

            with transaction.atomic():
                for row_index, row in enumerate(
                    sheet.iter_rows(min_row=2, values_only=True), start=2
                ):
                    data = dict(zip(import_order, row))

                    # Handle the unique ID
                    if data["id"] is None or data["id"] == "":
                        max_id += 1
                        data["id"] = max_id

                    # Convert date fields
                    for field in date_fields:
                        if field in data:
                            data[field] = convert_date(data[field])

                    # Convert decimal fields
                    for field, decimal_places in decimal_fields.items():
                        if field in data:
                            data[field] = convert_decimal(data[field], decimal_places)

                    # Handle foreign key relationships
                    try:
                        # Client foreign key
                        client_value = data.get("client")
                        if client_value:
                            client, created = Client.objects.get_or_create(client=client_value)
                            data["client"] = client

                        # Supplier foreign key
                        supplier_name = data.get("supplier")
                        if supplier_name:
                            supplier, created = Supplier.objects.get_or_create(
                                supplier=supplier_name
                            )
                            data["supplier"] = supplier

                        # Future Supplier foreign key
                        future_supplier_name = data.get("future_supplier")
                        if future_supplier_name:
                            future_supplier, created = Supplier.objects.get_or_create(
                                supplier=future_supplier_name
                            )
                            data["future_supplier"] = future_supplier

                        # Utility foreign key
                        utility_name = data.get("utility")
                        if utility_name:
                            utility, created = Utility.objects.get_or_create(utility=utility_name)
                            data["utility"] = utility

                        # Check if the record exists
                        existing_obj = Contract.objects.filter(id=data["id"]).first()

                        if existing_obj:
                            # Update existing record
                            for key, value in data.items():
                                setattr(existing_obj, key, value)
                            existing_obj.save()
                            self.stdout.write(
                                self.style.SUCCESS(f"Updated record with ID {existing_obj.id}")
                            )
                        else:
                            # Create new record
                            new_obj = Contract.objects.create(**data)
                            self.stdout.write(
                                self.style.SUCCESS(f"Created new record with ID {new_obj.id}")
                            )

                    except Exception as e:
                        error_message = f"Error processing record in row {row_index}: {str(e)}"
                        self.stdout.write(self.style.ERROR(error_message))
                        error_records.append({"row": row_index, "error": str(e), "data": data})

            # Write error records to CSV file
            if error_records:
                with open(error_log_path, "w", newline="") as csvfile:
                    fieldnames = ["row", "error", "data"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for record in error_records:
                        writer.writerow(record)
                self.stdout.write(
                    self.style.WARNING(
                        f"Errors encountered during import. Check {error_log_path} for details."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("Data import completed successfully with no errors.")
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {str(e)}"))
