SELECT
    display_name,
    interval '7 days'
      - COALESCE(
          (
              SELECT sum(upper(available_slot) - lower(available_slot))
              FROM unnest(
                  working_hours
                    * tstzmultirange(
                        tstzrange(
                            '2026-02-10 14:00+00',
                            '2026-02-17 14:00+00',
                            '[)'
                        )
                    )
              ) AS available_slot
          ),
          interval '0'
      ) AS total_unavailability
FROM scheduling.professionals
ORDER BY display_name;
