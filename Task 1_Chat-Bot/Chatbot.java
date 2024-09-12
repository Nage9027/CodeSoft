import java.util.Scanner;

public class Chatbot {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String rules = "hello|hi|hey:Hello! How can I assist you today?;" +
                       "how are you|what's up:I'm doing well, thanks! How about you?;" +
                       "what's your name:I'm a chatbot, nice to meet you!;" +
                       "help|assist:I can help with math, coding, and general questions. What do you need help with?;" +
                       "goodbye|bye|see you:Goodbye! It was nice chatting with you.;" +
                       "default:I didn't understand that. Can you please rephrase?";

        String[] rulePairs = rules.split(";");

        while (true) {
            System.out.print("You: ");
            String userInput = scanner.nextLine().toLowerCase();

            boolean matched = false;
            for (String rulePair : rulePairs) {
                String[] parts = rulePair.split(":");
                String pattern = parts[0];
                String response = parts[1];

                String[] words = pattern.split("\\|");
                for (String word : words) {
                    if (userInput.contains(word)) {
                        System.out.println("Chatbot: " + response);
                        matched = true;
                        break;
                    }
                }

                if (matched) {
                    break;
                }
            }

            if (!matched) {
                System.out.println("Chatbot: " + rulePairs[rulePairs.length - 1].split(":")[1]);
            }
        }
    }
}