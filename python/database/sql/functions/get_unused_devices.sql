CREATE OR REPLACE FUNCTION get_unused_devices(
    days_last_seen INT DEFAULT 90,
    exclude_adapter text DEFAULT 'sccm_adapter',
    exclude_user text DEFAULT 'loaner',
    exclude_notes text DEFAULT 'disabled'
)
RETURNS TABLE (
    computer_name VARCHAR,
    "user" VARCHAR,
    last_seen TIMESTAMP,
    seen_by VARCHAR,
    notes TEXT
)
LANGUAGE sql
AS $$
    SELECT DISTINCT
        wc.host_name AS computer_name,
        fiscal.user,
        wc.last_seen,
        wc.seen_by,
        wc.notes
    FROM windows_crowdstrike wc 
        INNER JOIN fiscal_inventory fiscal ON LOWER(TRIM(wc.host_name)) = LOWER(TRIM(fiscal.computer_name))
            WHERE wc.last_seen < CURRENT_DATE - (days_last_seen * INTERVAL '1 day')
            AND (
                wc.seen_by NOT ILIKE '%' || exclude_adapter || '%'
                OR wc.seen_by IS NULL
            )
            AND (
                fiscal.user NOT ILIKE '%' || exclude_user || '%'
                OR fiscal.user IS NULL
            )
            AND (
                wc.notes NOT ILIKE '%' || exclude_notes || '%'
                OR wc.notes IS NULL
            )
            ORDER BY wc.last_seen ASC;
$$;