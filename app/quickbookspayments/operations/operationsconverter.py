from app.quickbookspayments.httpclients.request.requesttype import RequestType

class OperationsConverter:
    @staticmethod
    def to_upper_case_class_name(name):
        """
        Convert a given name to its corresponding class name with the first letter capitalized.
        """
        return name.capitalize()

    @staticmethod
    def remove_null_from(obj):
        """
        Remove null values from an object recursively.
        """
        if isinstance(obj, dict):
            obj = {k: OperationsConverter.remove_null_from(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            obj = [OperationsConverter.remove_null_from(v) for v in obj if v is not None]
        return obj

    @staticmethod
    def get_json_from(obj):
        """
        Convert an object to JSON string after removing null values.
        """
        obj = OperationsConverter.remove_null_from(obj)
        return json.dumps(obj)

    @staticmethod
    def is_associated_array(data) -> bool:
        """
        Check if the provided data is an associative array.
        """
        if isinstance(data, dict):
            return all(isinstance(k, int) for k in data.keys())
        return False

    @staticmethod
    def object_from(body, type_):
        """
        Convert JSON string to an object of a given type.
        """
        array_represent = json.loads(body)
        if isinstance(array_represent, dict):
            class_name = getattr(ModulesConstants, 'NAMESPACE_MODULES') + type_
            if OperationsConverter.is_associated_array(array_represent):
                body = []
                for val in array_represent:
                    obj = globals()[class_name](val)
                    body.append(obj)
                return body
            else:
                obj = globals()[class_name](array_represent)
                return obj
        else:
            raise RuntimeError(f"Cannot convert {body} to Object.")

    @staticmethod
    def update_response_body_to_obj(response):
        """
        Update the response body to an object if the response is successful and has a body.
        """
        if not response.failed() and response.get_body():
            if response.get_associated_request().get_request_type() != RequestType.OAUTH:
                obj_body = OperationsConverter.object_from(response.get_body(),
                                                           response.get_associated_request().get_request_type())
                response.set_body(obj_body)

    @staticmethod
    def create_token_obj_from_value(val):
        from app.quickbookspayments.resolver import Token

        """
        Create a Token object from a given value.
        """
        return Token(val)
