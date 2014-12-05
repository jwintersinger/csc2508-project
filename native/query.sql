SELECT m1.data->'title', m2.data->'title'
FROM moviesj m1
JOIN moviesj m2 ON (m1.data->'id') > (m2.data->'id')
WHERE (
  SELECT COUNT(*) FROM (
    SELECT jsonb_array_elements(m1.data->'actors')
    INTERSECT
    SELECT jsonb_array_elements(m2.data->'actors')
  ) actors_intersection
) >= 1
AND ABS((m1.data->>'release_date')::date - (m2.data->>'release_date')::date) > 365*5;
