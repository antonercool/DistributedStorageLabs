import messages_pb2

if __name__ == '__main__': 
    # At the sender, instantiate the 'file' message class and fill it
    pb_file = messages_pb2.file()
    pb_file.id = 1
    pb_file.name = "test.pdf"
    pb_file.type = "application/pdf"
    pb_file.size = 123
    pb_file.created = 4
    # You don't have to set all fields
    # Serialize the file message to a string,
    # which can be transported over any protocol
    encoded_pb_file = pb_file.SerializeToString()
    print("Message:")
    print(pb_file)
    print("Encoded message:")
    print(f"{encoded_pb_file} ({len(encoded_pb_file)} bytes)")
    # ------- Send object --------

    # Server side
    pb_file2 = messages_pb2.file()
    pb_file2.ParseFromString(encoded_pb_file)
    # The parsed file has the same attributes as the original did
    assert(pb_file2.id == pb_file.id)
    assert(pb_file2.name == pb_file.name)
    assert(pb_file2.type == pb_file.type)
    assert(pb_file2.size == pb_file.size)
        
