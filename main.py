def greeting():
    print("-" * 60)
    print("🤖 Hi! Welcome to Cashflow. How can I assist you today?")
    print("Type an instruction or 'quit' to exit.\n")


def main():
    greeting()
    
    while True:
        user_input = input("> ")
        
        if user_input.lower() == 'quit':
            break
 
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
