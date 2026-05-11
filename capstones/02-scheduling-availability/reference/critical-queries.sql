WITH params AS (
    SELECT '00000000-0000-0000-0000-000000000201'::uuid AS professional_id,
           '2026-06-01'::date AS local_date
)
SELECT at.id, at.local_windows
FROM availability_templates at
JOIN params p ON p.professional_id = at.professional_id
WHERE at.day_of_week = extract(dow FROM p.local_date)::integer
  AND at.effective_during @> p.local_date;

WITH params AS (
    SELECT '00000000-0000-0000-0000-000000000201'::uuid AS professional_id,
           '00000000-0000-0000-0000-000000000301'::uuid AS patient_id,
           tstzrange('2026-06-01 15:00+00', '2026-06-01 15:30+00', '[)') AS slot
)
INSERT INTO appointments (professional_id, patient_id, slot, status)
SELECT professional_id, patient_id, slot, 'confirmed'
FROM params
WHERE EXISTS (SELECT 1 FROM professionals WHERE id = params.professional_id)
  AND EXISTS (SELECT 1 FROM patients WHERE id = params.patient_id)
ON CONFLICT DO NOTHING;

SELECT id, patient_id, lower(slot) AS starts_at, upper(slot) AS ends_at
FROM appointments
WHERE professional_id = '00000000-0000-0000-0000-000000000201'::uuid
  AND status = 'confirmed'
  AND lower(slot) >= now()
ORDER BY lower(slot)
LIMIT 50;

WITH cancelled AS (
    UPDATE appointments
    SET status = 'cancelled', cancelled_at = now()
    WHERE id = '00000000-0000-0000-0000-000000000401'::uuid
    RETURNING professional_id, slot
),
next_waiting AS (
    SELECT w.id
    FROM waitlist_entries w
    JOIN cancelled c ON c.professional_id = w.professional_id
    WHERE w.status = 'waiting'
    ORDER BY w.created_at
    LIMIT 1
)
UPDATE waitlist_entries w
SET status = 'offered'
FROM next_waiting nw
WHERE w.id = nw.id
RETURNING w.id, w.patient_id;

SELECT id, patient_id, desired_slot, created_at
FROM waitlist_entries
WHERE professional_id = '00000000-0000-0000-0000-000000000201'::uuid
  AND status = 'waiting'
ORDER BY created_at;

SELECT id, display_name, specialties
FROM professionals
WHERE search_vector @@ plainto_tsquery('english', 'cardiology')
ORDER BY display_name
LIMIT 20;
