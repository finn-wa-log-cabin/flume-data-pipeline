from typing import List


class MockOut:
    value: List[str]

    def set(self, val: List[str]) -> None:
        self.value = val

    def get(self) -> List[str]:
        return self.value
