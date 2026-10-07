from app.schemas.term import FinancialTerm


TERMS = {
    "eir": FinancialTerm(
        code="EIR",
        name="Effective Interest Rate",
        name_ru="Эффективная процентная ставка",
        category="lending",
        description=(
            "Ставка, отражающая фактическую стоимость кредита "
            "с учетом связанных денежных потоков."
        ),
    ),

    "pd": FinancialTerm(
        code="PD",
        name="Probability of Default",
        name_ru="Вероятность дефолта",
        category="risk",
        description=(
            "Вероятность того, что заемщик перейдет "
            "в состояние дефолта за определенный период."
        ),
    ),

    "lgd": FinancialTerm(
        code="LGD",
        name="Loss Given Default",
        name_ru="Убыток при дефолте",
        category="risk",
        description=(
            "Доля задолженности, которую кредитор потеряет "
            "при наступлении дефолта."
        ),
    ),
}


class DictionaryService:

    def get_term(
        self,
        term: str,
    ) -> FinancialTerm | None:

        return TERMS.get(
            term.lower().strip()
        )

    def search(
        self,
        query: str,
    ) -> list[FinancialTerm]:

        query = query.lower().strip()

        result = []

        for term in TERMS.values():

            searchable = " ".join(
                [
                    term.code,
                    term.name,
                    term.name_ru,
                    term.category,
                    term.description,
                ]
            ).lower()

            if query in searchable:
                result.append(term)

        return result