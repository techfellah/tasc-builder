from __future__ import annotations

from ..exceptions import PromptRenderException
from ..interfaces import IPromptService
from ..models import PromptRenderRequest, RenderedPrompt


class PromptService(IPromptService):
    """Render Prompt templates with supplied values."""

    def render(self, request: PromptRenderRequest) -> RenderedPrompt:
        self._validate_required_variables(request)

        try:
            return RenderedPrompt(
                system_prompt=request.template.system_prompt.format(**request.values),
                user_prompt=request.template.user_prompt.format(**request.values),
                variables=dict(request.values),
            )
        except Exception as exception:
            raise PromptRenderException("Prompt rendering failed") from exception

    @staticmethod
    def _validate_required_variables(request: PromptRenderRequest) -> None:
        for variable in request.template.variables:
            if variable.required and variable.name not in request.values:
                raise PromptRenderException(
                    f"Required prompt variable is missing: {variable.name}"
                )
