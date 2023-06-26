from sqlalchemy import text

FUNCTION_SET_COSTS = text("""
    CREATE OR REPLACE FUNCTION set_costs(att_id_in int) RETURNS VOID AS $$
    DECLARE
    academic_title_var VARCHAR(50);
    costs_var INT;
    banquet BOOLEAN;
    tour BOOLEAN;
    single_room_nights INT;
    double_room_nights INT;
    
    BEGIN
    SELECT academic_title, costs, is_banquet, is_tour INTO academic_title_var, costs_var, banquet, tour FROM attendants WHERE att_id = att_id_in;
    SELECT COUNT(att_quantity) INTO single_room_nights FROM rents, rooms WHERE rents.att_id = att_id_in AND rooms.room_number = rents.room_number AND att_quantity = 1;
    SELECT COUNT(att_quantity) INTO double_room_nights FROM rents, rooms WHERE rents.att_ID = att_id_in AND rooms.room_number = rents.room_number AND att_quantity = 2;

    costs_var := single_room_nights * 200 + double_room_nights * 100;

    IF academic_title_var IS NOT NULL THEN
        costs_var := costs_var + 1000;
    ELSE
        costs_var := costs_var + 500;
    END IF;

    IF banquet THEN
        costs_var := costs_var + 150;
    END IF;

    IF tour THEN 
        costs_var := costs_var + 50;
    END IF;

    UPDATE attendants SET costs = costs_var WHERE att_id = att_id_in;
    END;
    $$ LANGUAGE plpgsql;
""")

TRIGGERS_AFTER_INSERT_RENTS_ATTENDANTS = text("""
    CREATE OR REPLACE FUNCTION after_rent_insert_trigger()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM set_costs(NEW.att_id);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER after_rent_insert
    AFTER INSERT ON rents
    FOR EACH ROW
    EXECUTE FUNCTION after_rent_insert_trigger();

    CREATE OR REPLACE FUNCTION after_attendant_insert_trigger()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM set_costs(NEW.att_id);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER after_attendant_insert
    AFTER INSERT ON attendants
    FOR EACH ROW
    EXECUTE FUNCTION after_attendant_insert_trigger();
""")