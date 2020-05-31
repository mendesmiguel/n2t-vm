import re
from dataclasses import dataclass
from enum import Enum
from textwrap import dedent
from typing import List, Optional


def clean(ins: str) -> List[str]:
    for line in ins.split("\n"):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        line = " ".join(re.split(r"\s+", line, flags=re.UNICODE))
        yield line


def clean_instructions(ins: str, to_lower: bool = False) -> str:
    inst = "\n".join(clean(ins))
    return inst.lower() if to_lower else inst


class Command(Enum):
    PUSH = 1
    POP = 2
    ADD = 3
    SUB = 4
    NEG = 5
    EQ = 6
    GT = 7
    LT = 8
    AND = 9
    OR = 10
    NOT = 11


class Segment(Enum):
    CONSTANT = 1


@dataclass
class ByteCodeInst:
    _SYMBOL_TABLE = {
        "push": Command.PUSH,
        "pop": Command.POP,
        "add": Command.ADD,
        "sub": Command.SUB,
        "neg": Command.NEG,
        "eq": Command.EQ,
        "constant": Segment.CONSTANT,
    }

    cmd: Command
    segment: Optional[Segment] = None
    value: Optional[int] = None

    @classmethod
    def from_string(cls, line: str) -> "ByteCodeInst":
        tokens = line.split()
        try:
            raw_cmd, raw_seg, value = tokens
            cmd = cls._SYMBOL_TABLE[raw_cmd]
            segment = cls._SYMBOL_TABLE[raw_seg]
            value = int(value)
            return cls(cmd, segment, value)
        except ValueError:
            cmd = cls._SYMBOL_TABLE[tokens[0]]
            return cls(cmd)

    def to_assembly(self) -> str:
        """
        Returns a clean set of assembly instructions that performs
        the byte code operation.
        """
        if self.cmd == Command.PUSH and self.segment.CONSTANT:
            inst = self._build_push_constant()
        elif self.cmd == Command.ADD:
            inst = self._build_add()
        elif self.cmd == Command.SUB:
            inst = self._build_sub()
        elif self.cmd == Command.EQ:
            inst = self._build_eq()
        else:
            raise ValueError("Unsupported command.")

        return clean_instructions(inst)

    def _build_push_constant(self) -> str:
        """
        *SP = value
        SP++
        """
        value = self.value
        return dedent(
            f"""
            @{value}
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
        )

    def _build_add(self) -> str:
        """
        SP--
        temp0 = *SP
        SP--
        *SP = *SP - temp0
        SP++
        """
        return dedent(
            """
            @SP
            M=M-1
            A=M
            D=M
            @SP
            M=M-1
            A=M
            M=M+D
            @SP
            M=M+1
            """
        )

    def _build_sub(self) -> str:
        """
        SP--
        temp0 = *SP
        SP--
        *SP = *SP - temp0
        SP++
        """
        return dedent(
            """
            @SP
            M=M-1
            A=M
            D=M
            @SP
            M=M-1
            A=M
            M=M-D
            @SP
            M=M+1
            """
        )

    def _build_eq(self) -> str:
        """
        eq -> x==0


        SP--
        temp0 = *SP
        SP--
        *SP = 0 == temp0
        SP++
        """
        return dedent(
            """
            // SP--
            @SP
            M=M-1
            // D = *SP
            A=M
            D=M
            // SP--
            @SP
            M=M-1
            // *SP = !*SP
            A=M
            M=!M
            // D = D & *SP
            D=D&M
            
            // if D == 0
            @EQUAL
            D;JEQ
            // else
            @NOT_EQUAL
            D;JNE
            
            (EQUAL)
            // True in Hack ASM is -1
            @SP
            A=M
            M=-1
            // SP++
            @SP
            M=M+1
            
            (NOT_EQUAL)
            // False in Hack ASM is 0
            @SP
            A=M
            M=0
            // SP++
            @SP
            M=M+1
            """
        )


def parse(ins: str) -> List[ByteCodeInst]:
    for line in ins.split("\n"):
        yield ByteCodeInst.from_string(line)
