from mcp.server import MCPServer

from app.services.dictionary_service import DictionaryService


service = DictionaryService()


def register_dictionary_tools(
    mcp: MCPServer,
):

    @mcp.tool()
    def get_financial_term(
        term: str,
    ) -> dict:
        """
        Get information about a financial or banking term.

        Use this tool when the user asks what a specific
        financial abbreviation or financial term means.
        """

        result = service.get_term(term)

        if result is None:
            return {
                "found": False,
                "query": term,
                "message": "Financial term not found",
            }

        return {
            "found": True,
            **result.model_dump(),
        }


    @mcp.tool()
    def search_financial_terms(
        query: str,
    ) -> list[dict]:
        """
        Search MoneySense financial terminology.

        Search by abbreviation, financial name,
        Russian name, category or description.
        """

        results = service.search(query)

        return [
            item.model_dump()
            for item in results
        ]