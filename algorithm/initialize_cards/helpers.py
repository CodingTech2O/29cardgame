def take_input_from_user(inp,tye=str):
    while True:
        try:
            return tye(input(inp))
        except Exception:
            display_output_to_user(f"This input wasn't valid type. ")
def display_output_to_user(out):
    print(out) 
    return out