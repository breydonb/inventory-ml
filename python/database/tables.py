from database.schema import Column, Table

INVENTORY_TABLE = Table(
    name="inventory",
    columns=[
        Column("item_id", "INTEGER GENERATED ALWAYS AS IDENTITY", primary_key=True, nullable=False, csv_name=None),
        Column("computer_name", "VARCHAR(255)", nullable=False, csv_name="COMPUTER-NAME"),
        Column("serial_number", "VARCHAR(255)", nullable=False, csv_name="SERIAL#"),
        Column("P-TAG", "VARCHAR(255)", nullable=True, csv_name="PTAG"),
        Column("user", "VARCHAR(255)", nullable=False, csv_name="USER"),
        Column("location", "VARCHAR(255)", nullable=False, csv_name="LOCATION"),
        Column("model", "VARCHAR(255)", nullable=False, csv_name="MODEL"),
        Column("date_added", "DATE", nullable=True, csv_name="Age"),
        Column("type", "VARCHAR(255)", nullable=False, csv_name="Type"),
        Column("mac_or_pc", "VARCHAR(255)", nullable=False, csv_name="Mac / PC"),
        Column("department", "VARCHAR(255)", nullable=False, csv_name="DEPT")
    ]
)

FISICAL_INVENTORY_TABLE = Table(
    name="fiscal_inventory",
    columns=[
        Column("item_id", "INTEGER GENERATED ALWAYS AS IDENTITY", primary_key=True, nullable=False, csv_name=None),
        Column("computer_name", "VARCHAR(255)", nullable=False, csv_name="ComputerName"),
        Column("serial_number", "VARCHAR(255)", nullable=False, csv_name="SerialNumber"),
        Column("P-TAG", "VARCHAR(255)", nullable=True, csv_name="PTAG"),
        Column("user", "VARCHAR(255)", nullable=False, csv_name="User"),
        Column("location", "VARCHAR(255)", nullable=False, csv_name="Location"),
        Column("model", "VARCHAR(255)", nullable=False, csv_name="Model"),
        Column("cost_center", "VARCHAR(255)", nullable=False, csv_name="CostCenter"),
        Column("type", "VARCHAR(255)", nullable=True, csv_name="Type")
    ]
)

WINDOWS_CROWDSTRIKE_TABLE = Table(
    name="windows_crowdstrike",
    columns=[
        Column("host_name", "VARCHAR(255)", nullable=False, primary_key=True, csv_name="Host Name"),
        Column("seen_by", "VARCHAR(255)", nullable=False, csv_name="Seen By"),
        Column("windows_version", "VARCHAR(255)", nullable=False, csv_name="Windows Version"),
        Column("last_seen", "TIMESTAMP", nullable=False, csv_name="Last Seen"),
        Column("unit", "VARCHAR(255)", nullable=True, csv_name="Unit"),
        Column("notes", "TEXT", nullable=True, csv_name="Notes")
    ]
)

ALL_TABLES: list[Table] = [
    INVENTORY_TABLE,
    WINDOWS_CROWDSTRIKE_TABLE,
    FISICAL_INVENTORY_TABLE
]

CSV_IMPORTS: tuple[Table, str] = (
    (INVENTORY_TABLE, "data/2025Inventory.csv"),
    (WINDOWS_CROWDSTRIKE_TABLE, "data/WindowsCrowdStrikeEnrollmentTable.csv"),
    (FISICAL_INVENTORY_TABLE, "data/FY27InventoryComparison.csv")
)