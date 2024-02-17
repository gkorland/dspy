import pytest
import dsp
from dspy import Predict, Signature
from dspy.utils.dummies import DummyLM

def test_initialization_with_string_signature():
    signature_string = "input1, input2 -> output"
    predict = Predict(signature_string)
    expected_instruction = "Given the fields `input1`, `input2`, produce the fields `output`."
    assert predict.signature.instructions == expected_instruction
    assert predict.signature.instructions == Signature(signature_string).instructions

def test_reset_method():
    predict_instance = Predict("input -> output")
    predict_instance.lm = "modified"
    predict_instance.traces = ["trace"]
    predict_instance.train = ["train"]
    predict_instance.demos = ["demo"]
    predict_instance.reset()
    assert predict_instance.lm is None
    assert predict_instance.traces == []
    assert predict_instance.train == []
    assert predict_instance.demos == []

def test_dump_and_load_state():
    predict_instance = Predict("input -> output")
    predict_instance.lm = "lm_state"
    dumped_state = predict_instance.dump_state()
    new_instance = Predict("input -> output")
    new_instance.load_state(dumped_state)
    assert new_instance.lm == "lm_state"

def test_call_method():
    predict_instance = Predict("input -> output")
    dsp.settings.lm = DummyLM(["test output"])
    result = predict_instance(input="test input")
    assert result.output == "test output"
    assert dsp.settings.lm.get_convo(-1) == (
        "Given the fields `input`, produce the fields `output`.\n"
        "\n---\n\n"
        "Follow the following format.\n\n"
        "Input: ${input}\n"
        "Output: ${output}\n"
        "\n---\n\n"
        "Input: test input\n"
        "Output: test output"
    )

def test_forward_method():
    program = Predict("question -> answer")
    dsp.settings.lm = DummyLM([])
    result = program(question="What is 1+1?").answer
    assert result == "No more responses"

def test_forward_method2():
    program = Predict("question -> answer1, answer2")
    dsp.settings.lm = DummyLM(["my first answer", "my second answer"])
    result = program(question="What is 1+1?")
    assert result.answer1 == "my first answer"
    assert result.answer2 == "my second answer"

def test_config_management():
    predict_instance = Predict("input -> output")
    predict_instance.update_config(new_key="value")
    config = predict_instance.get_config()
    assert "new_key" in config and config["new_key"] == "value"

