class EnergyTools:
    LIGHT = {    }
    AIR_CONDITIONER = {    }
    ROOM = ["living_room", "bedroom", "kitchen"]
    HISTORICAL_DATA = [
        {
            "device": "LIGHT",
            "room": "living_room",
            "status": "ON",
            "time": "2025-06-21T18:00:00",
            "note": "Turned on as it got dark"
        },
        {
            "device": "LIGHT",
            "room": "living_room",
            "status": "OFF",
            "time": "2025-06-21T23:00:00",
            "note": "User went to bed"
        },
        {
            "device": "AIR_CONDITIONER",
            "room": "bedroom",
            "status": "ON",
            "time": "2025-06-21T22:30:00",
            "note": "Turned on before sleep"
        },
        {
            "device": "AIR_CONDITIONER",
            "room": "bedroom",
            "status": "OFF",
            "time": "2025-06-22T06:30:00",
            "note": "Turned off after waking up"
        },
        {
            "device": "LIGHT",
            "room": "kitchen",
            "status": "ON",
            "time": "2025-06-22T06:45:00",
            "note": "Turned on during breakfast"
        },
        {
            "device": "LIGHT",
            "room": "kitchen",
            "status": "OFF",
            "time": "2025-06-22T07:30:00",
            "note": "Turned off after leaving the kitchen"
        },
        {
            "device": "LIGHT",
            "room": "living_room",
            "status": "ON",
            "time": "2025-06-22T18:10:00",
            "note": "Turned on at sunset"
        },
        {
            "device": "LIGHT",
            "room": "living_room",
            "status": "OFF",
            "time": "2025-06-22T23:15:00",
            "note": "Turned off before sleep"
        },
        {
            "device": "AIR_CONDITIONER",
            "room": "bedroom",
            "status": "ON",
            "time": "2025-06-22T22:20:00",
            "note": "Scheduled cooling before sleep"
        },
        {
            "device": "AIR_CONDITIONER",
            "room": "bedroom",
            "status": "OFF",
            "time": "2025-06-23T06:40:00",
            "note": "Auto-off after scheduled sleep period"
        }
    ]

    @classmethod
    def change_light_status(cls, room: str, status: str) -> str:
        """
        Change the status of the light in a specified room.
        Args:
            room (str): The room where the light is located.
            status (str): The desired status of the light ('ON' or 'OFF').
        Returns:
            str: A message indicating the result of the operation.
        """

        if room not in cls.ROOM:
            return f"Invalid room: {room}. Available rooms are {cls.ROOM}."
        current_status = cls.LIGHT.get(room, "OFF")
        if current_status == status:
            return f"Light in {room} is already {status}."
        cls.LIGHT[room] = status
        return f"Light in {room} is now {status}."

    @classmethod
    def change_air_conditioner_status(cls, room: str, status: str) -> str:
        """ 
        Change the status of the air conditioner in a specified room.
        Args:
            room (str): The room where the air conditioner is located.
            status (str): The desired status of the air conditioner ('ON' or 'OFF').
        Returns:
            str: A message indicating the result of the operation.
        """

        if room not in cls.ROOM:
            return f"Invalid room: {room}. Available rooms are {cls.ROOM}."
        current_status = cls.AIR_CONDITIONER.get(room, "OFF")
        if current_status == status:
            return f"Air conditioner in {room} is already {status}."
        cls.AIR_CONDITIONER[room] = status
        return f"Air conditioner in {room} is now {status}."
    
    @classmethod
    def get_historical_data(cls) -> list:
        """
        Retrieve historical data of device usage.
        Returns:
            list: A list of dictionaries containing historical data of device usage.
        """
        
        return cls.HISTORICAL_DATA


