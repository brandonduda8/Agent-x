class GenesisSkillAnalyzer:


    def analyze(
        self,
        mission
    ):

        mission_text = mission.lower()

        skills = []


        if any(word in mission_text for word in [
            "research",
            "find",
            "analyze"
        ]):

            skills.append("research")


        if any(word in mission_text for word in [
            "build",
            "code",
            "software",
            "deploy"
        ]):

            skills.append("coding")


        if any(word in mission_text for word in [
            "client",
            "sales",
            "revenue",
            "customer"
        ]):

            skills.append("revenue")


        if any(word in mission_text for word in [
            "learn",
            "optimize",
            "improve"
        ]):

            skills.append("learning")


        if not skills:

            skills.append("execution")


        return skills
