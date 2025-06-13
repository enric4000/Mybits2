from Apps.warehouse.models import Luggage, Warehouse


class WarehouseService():
    @staticmethod
    def create_warehouse(form, event):
        """
        Creates a new warehouse based on the provided form and event.
        """
        warehouse = form.save(commit=False)
        warehouse.event = event
        warehouse.save()
        return warehouse

    @staticmethod
    def search_warehouses(event, search_term):
        """
        Searches for warehouses associated with a specific event based on a search term.
        """
        return Warehouse.objects.filter(event=event, name__icontains=search_term)

    @staticmethod
    def get_warehouses(event):
        """
        Retrieves all warehouses associated with a specific event.
        """
        return Warehouse.objects.filter(event=event)

    @staticmethod
    def get_warehouse(warehouse_id):
        """
        Retrieves a warehouse by its ID.
        """
        return Warehouse.objects.get(id=warehouse_id)

    @staticmethod
    def update_warehouse(form, warehouse):
        """
        Updates an existing warehouse with the provided form data.
        """
        if warehouse:
            for key, value in form.cleaned_data.items():
                setattr(warehouse, key, value)
            warehouse.save()
            return warehouse

        return None

    @staticmethod
    def delete_warehouse(warehouse):
        """
        Deletes a warehouse by its ID.
        """
        if warehouse is None or warehouse.luggage.count() > 0:
            return False

        warehouse.delete()
        return True

    @staticmethod
    def get_warehouse_luggage(warehouse):
        """
        Retrieves all luggage items associated with a specific warehouse.
        """
        if warehouse is None:
            return []

        luggage = warehouse.luggage.order_by('row_position', 'column_position')
        return luggage

    @staticmethod
    def create_luggage(form, warehouse, participant):
        """
        Creates a new luggage item in the specified warehouse.
        """
        if warehouse is None or participant is None:
            return None

        luggage = form.save(commit=False)
        luggage.owner = participant
        
        if warehouse.luggage.filter(
            row_position=luggage.row_position,
            column_position=luggage.column_position
        ).exists():
            return None

        if luggage.row_position > warehouse.rows or luggage.column_position > warehouse.columns:
            return None

        luggage.save()
        warehouse.luggage.add(luggage)
        return luggage

    @staticmethod
    def get_luggage(luggage_id):
        """
        Retrieves a luggage item by its ID.
        """
        return Luggage.objects.get(id=luggage_id)

    @staticmethod
    def update_luggage(form, luggage, warehouse):
        """
        Updates an existing luggage item with the provided form data.
        """
        if luggage:
            for key, value in form.cleaned_data.items():
                setattr(luggage, key, value)

            if warehouse.luggage.filter(
                row_position=luggage.row_position,
                column_position=luggage.column_position
            ).exclude(id=luggage.id).exists():
                return None

            if luggage.row_position > warehouse.rows or luggage.column_position > warehouse.columns:
                return None

            luggage.save()
            return luggage

        return None

    @staticmethod
    def delete_luggage(luggage, warehouse):
        """
        Deletes a luggage item by its ID.
        """
        if luggage is None:
            return False
        
        warehouse.luggage.remove(luggage)
        luggage.delete()
        return True

    @staticmethod
    def get_warehouse_luggage_by_participant(warehouse, participant):
        """
        Retrieves all luggage items associated with a specific participant in a warehouse.
        """
        if warehouse is None or participant is None:
            return []

        return warehouse.luggage.filter(owner=participant).order_by('row_position', 'column_position')
