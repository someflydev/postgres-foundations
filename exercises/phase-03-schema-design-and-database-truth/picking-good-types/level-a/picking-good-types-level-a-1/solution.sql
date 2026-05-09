DROP TABLE IF EXISTS ecommerce.picking_good_types_a_1;
CREATE TABLE ecommerce.picking_good_types_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    description text,
    amount numeric(12,2),
    measured_at timestamptz,
    is_billable boolean
);

ALTER TABLE ecommerce.picking_good_types_a_1
    ALTER COLUMN description SET NOT NULL,
    ALTER COLUMN amount SET NOT NULL,
    ALTER COLUMN measured_at SET DEFAULT now(),
    ALTER COLUMN measured_at SET NOT NULL,
    ALTER COLUMN is_billable SET DEFAULT true,
    ALTER COLUMN is_billable SET NOT NULL;

ALTER TABLE ecommerce.picking_good_types_a_1
    ADD CONSTRAINT picking_good_types_a_1_amount_nonnegative CHECK (amount >= 0);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'picking_good_types_a_1'
ORDER BY table_name;
