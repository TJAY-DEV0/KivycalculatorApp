class BracketChecker:
    def __init__(self):
        self.bracket_map = {')': '(', '}': '{', ']': '['}

    def check_brackets(self, input_str):
        stack = []
        result = list(input_str)
        for char in input_str:
            if char in self.bracket_map.values():
                stack.append(char)
            elif char in self.bracket_map.keys():
                if stack and stack[-1] == self.bracket_map[char]:
                    stack.pop()
        while stack:
            bracket = stack.pop()
            if bracket == '(':
                result.append(')')
            elif bracket == '{':
                result.append('}')
            elif bracket == '[':
                result.append(']')
        return ''.join(result)
