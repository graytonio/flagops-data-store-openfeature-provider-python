import typing
from openfeature.flag_evaluation import FlagResolutionDetails
import requests

from openfeature.provider.metadata import Metadata
from openfeature.provider.provider import AbstractProvider
from openfeature.evaluation_context import EvaluationContext

class FlagOpsProvider(AbstractProvider):
    def __init__(
        self,
        baseURL: str,
        provider: AbstractProvider
    ):
        self.baseURL = baseURL
        self.provider = provider
    
    def get_metadata(self) -> Metadata:
        return Metadata(name="FlagOpsProvider")
    
    def get_identity_context(self, id: str) -> typing.Dict[str, str]:
        resp = requests.get(f"{self.baseURL}/fact/{id}")
        facts = resp.json()
        return facts
    
    def inject_identity_context(self, ctx: typing.Dict[str, str], eval_ctx: EvaluationContext) -> EvaluationContext:
        eval_ctx.attributes.update(ctx)
        return eval_ctx

    def resolve_boolean_details(self, flag_key: str, default_value: bool, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails[bool]:
        if evaluation_context.targeting_key == None:
            return self.provider.resolve_boolean_details(flag_key, default_value, evaluation_context)
        
        ctx = self.get_identity_context(evaluation_context.targeting_key)
        return self.provider.resolve_boolean_details(flag_key, default_value, self.inject_identity_context(ctx, evaluation_context))
    
    def resolve_integer_details(self, flag_key: str, default_value: int, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails[int]:
        if evaluation_context.targeting_key == None:
            return self.provider.resolve_integer_details(flag_key, default_value, evaluation_context)
        
        ctx = self.get_identity_context(evaluation_context.targeting_key)
        return self.provider.resolve_integer_details(flag_key, default_value, self.inject_identity_context(ctx, evaluation_context))
    
    def resolve_float_details(self, flag_key: str, default_value: float, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails[float]:
        if evaluation_context.targeting_key == None:
            return self.provider.resolve_float_details(flag_key, default_value, evaluation_context)
        
        ctx = self.get_identity_context(evaluation_context.targeting_key)
        return self.provider.resolve_float_details(flag_key, default_value, self.inject_identity_context(ctx, evaluation_context))
    
    def resolve_string_details(self, flag_key: str, default_value: str, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails[str]:
        if evaluation_context.targeting_key == None:
            return self.provider.resolve_string_details(flag_key, default_value, evaluation_context)
        
        ctx = self.get_identity_context(evaluation_context.targeting_key)
        return self.provider.resolve_string_details(flag_key, default_value, self.inject_identity_context(ctx, evaluation_context))
    
    def resolve_object_details(self, flag_key: str, default_value: dict | list, evaluation_context: EvaluationContext | None = None) -> FlagResolutionDetails[dict | list]:
        if evaluation_context.targeting_key == None:
            return self.provider.resolve_object_details(flag_key, default_value, evaluation_context)
        
        ctx = self.get_identity_context(evaluation_context.targeting_key)
        return self.provider.resolve_object_details(flag_key, default_value, self.inject_identity_context(ctx, evaluation_context))
    