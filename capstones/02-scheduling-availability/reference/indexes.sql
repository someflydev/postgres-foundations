-- Q1 provider availability lookup by day and effective date.
CREATE INDEX availability_templates_professional_day_idx
    ON availability_templates (professional_id, day_of_week);

-- Q1 blackout overlap checks.
CREATE INDEX blackout_windows_professional_slot_idx
    ON blackout_windows USING gist (professional_id, slot);

-- Q2/Q3 confirmed appointment lookup; exclusion constraint owns overlap correctness.
CREATE INDEX appointments_professional_lower_slot_idx
    ON appointments (professional_id, lower(slot))
    WHERE status = 'confirmed';

-- Q4/Q5 waitlist promotion by provider and arrival order.
CREATE INDEX waitlist_professional_waiting_idx
    ON waitlist_entries (professional_id, created_at)
    WHERE status = 'waiting';

-- Optional FTS over professional bios and specialties.
CREATE INDEX professionals_search_vector_idx ON professionals USING gin (search_vector);
