import pathlib

from translator.parser import parse, clean_instructions

PROJECT_07_DIR = pathlib.Path("/home/miguel/nand2tetris/projects/07")
SIMPLE_ADD_DIR = PROJECT_07_DIR / pathlib.Path("StackArithmetic/SimpleAdd")
STACK_TEST_DIR = PROJECT_07_DIR / pathlib.Path("StackArithmetic/StackTest")
POINTER_TEST_DIR = PROJECT_07_DIR / pathlib.Path("MemoryAccess/PointerTest")
BASIC_TEST_DIR = PROJECT_07_DIR / pathlib.Path("MemoryAccess/BasicTest")
STATIC_TEST_DIR = PROJECT_07_DIR / pathlib.Path("MemoryAccess/StaticTest")

TEST_CODE_DIR = PROJECT_07_DIR / "test_code"

SIMPLE_ADD = SIMPLE_ADD_DIR / "SimpleAdd.vm"
SIMPLE_ADD_ASM = SIMPLE_ADD_DIR / "SimpleAdd.asm"

STACK_TEST = STACK_TEST_DIR / "StackTest.vm"
STACK_TEST_ASM = STACK_TEST_DIR / "StackTest.asm"


POINTER_TEST = POINTER_TEST_DIR / "PointerTest.vm"
POINTER_TEST_ASM = POINTER_TEST_DIR / "PointerTest.asm"

STATIC_TEST = STATIC_TEST_DIR / "StaticTest.vm"
STATIC_TEST_ASM = STATIC_TEST_DIR / "StaticTest.asm"

BASIC_TEST = BASIC_TEST_DIR / "BasicTest.vm"
BASIC_TEST_ASM = BASIC_TEST_DIR / "BasicTest.asm"


TEST_EQ = TEST_CODE_DIR / "test_eq/test_eq.vm"
TEST_EQ_ASM = TEST_CODE_DIR / "test_eq/test_eq.asm"

TEST_LT = TEST_CODE_DIR / "test_lt/test_lt.vm"
TEST_LT_ASM = TEST_CODE_DIR / "test_lt/test_lt.asm"

TEST_GT = TEST_CODE_DIR / "test_gt/test_gt.vm"
TEST_GT_ASM = TEST_CODE_DIR / "test_gt/test_gt.asm"

TEST_NOT = TEST_CODE_DIR / "test_not/test_not.vm"
TEST_NOT_ASM = TEST_CODE_DIR / "test_not/test_not.asm"

TEST_NEG = TEST_CODE_DIR / "test_neg/test_neg.vm"
TEST_NEG_ASM = TEST_CODE_DIR / "test_neg/test_neg.asm"

seg = "static"

TEST_LATEST = TEST_CODE_DIR / f"test_{seg}/test_{seg}.vm"
TEST_LATEST_ASM = TEST_CODE_DIR / f"test_{seg}/test_{seg}.asm"


def translate(inst: str) -> str:
    cleaned_inst = clean_instructions(inst, to_lower=True)
    byte_codes = parse(cleaned_inst, filename="test_static")
    return "\n".join([byte_code.to_asm() for byte_code in byte_codes])


if __name__ == "__main__":
    with open(POINTER_TEST) as f:
        inst = f.read()

    with open(POINTER_TEST_ASM, "w") as f:
        s = translate(inst)
        f.write(s)
        print(s)
