DROP FUNCTION IF EXISTS generate_public_id;

CREATE FUNCTION generate_public_id(tbl_name text, public_id_len integer)
RETURNS text
LANGUAGE plpgsql
AS $$
DECLARE
    public_id text := '';
    number_random integer := 0;
    public_id_exist text;
    is_loop boolean := true;
BEGIN
    WHILE is_loop LOOP
        public_id := '';
        FOR counter IN 1..public_id_len LOOP
            number_random := floor(random() * 10);
            IF number_random % 2 = 0 THEN
                public_id := CONCAT(public_id, CHR( (65 + floor(random() * 26))::integer ));
            ELSEIF number_random % 3 = 0 THEN
                public_id := CONCAT(public_id, CHR( (97 + floor(random() * 26))::integer ));
            ELSE
                public_id := CONCAT(public_id, CHR( (48 + floor(random() * 10))::integer ));
            END IF;
        END LOOP;

        EXECUTE FORMAT('SELECT public_id FROM %I WHERE public_id = $1', tbl_name)
        INTO public_id_exist
        USING public_id;

        IF public_id_exist IS NULL THEN
            is_loop := false;
        END IF;
    END LOOP;

--     RAISE NOTICE 'The result is %', public_id;

    RETURN public_id;
END;
$$;