

-- Select data that we are going to be using
SELECT location
	 , date
	 , total_cases
	 , new_cases
	 , total_deaths
	 , population
FROM CovidPortfolioProject..CovidDeaths
ORDER BY 1,2


-- Total Cases vs Total Deaths
-- Showing likelihood of dying if you contract COVID in your country
SELECT location
     , date
	 , total_cases
	 , total_deaths
	 , (total_deaths/total_cases)*100 as death_percentage
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is not null
ORDER BY 1,2


-- Total Cases vs Population
-- Percent of population that contracted COVID
SELECT location
     , date
	 , total_cases
	 , population
	 , (total_cases/population)*100 as percent_population_infected
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is not null
ORDER BY 1,2


-- Countries with Highest Infection Rate Compared to Population
SELECT location
     , MAX(total_cases) as highest_infection_count
	 , population
	 , MAX((total_cases/population))*100 as case_percentage
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is not null
GROUP BY location, population
ORDER BY case_percentage DESC


-- Showing Countries with Highest Deaths per Population
SELECT location
     , MAX(cast(total_deaths as int)) as total_death_count
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is not null
GROUP BY location
ORDER BY total_death_count DESC


-- Showing Continent with Highest Deaths Per Population
SELECT location
     , MAX(cast(total_deaths as int)) as total_death_count
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is null
GROUP BY location
ORDER BY total_death_count DESC


-- GLOBAL NUMBERS
SELECT date
	 , SUM(new_cases) as total_cases
	 , SUM(cast(new_deaths as int)) as total_deaths
	 , SUM(cast(new_deaths as int)) / SUM(new_cases) *100 as DeathPercentage
FROM CovidPortfolioProject..CovidDeaths
WHERE continent is not null
GROUP BY date
ORDER BY 1,2

-- Total Population vs Vaccinations
-- USING CTE
WITH PopVsVac (Continent, Location, Date, Population, NewVaccinations, RollingPeopleVaccinated)
AS
(
SELECT dea.continent
	 , dea.location
	 , dea.date
	 , dea.population
	 , vac.new_vaccinations
	 , SUM(cast(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_people_vaccinated
FROM CovidPortfolioProject..CovidDeaths dea
JOIN CovidPortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)

SELECT *, (RollingPeopleVaccinated/Population)*100 AS RollingPercentageVaccinated
FROM PopVsVac

-- Total Poplation vs Vaccinations
-- USING TEMP TABLE
DROP TABLE IF EXISTS #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
NewVaccinations numeric,
RollingPeopleVaccinated numeric,
)

INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent
	 , dea.location
	 , dea.date
	 , dea.population
	 , vac.new_vaccinations
	 , SUM(cast(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_people_vaccinated
FROM CovidPortfolioProject..CovidDeaths dea
JOIN CovidPortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT *, (RollingPeopleVaccinated/Population)*100
FROM #PercentPopulationVaccinated



-- Creating view to store for later viz

CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent
	 , dea.location
	 , dea.date
	 , dea.population
	 , vac.new_vaccinations
	 , SUM(cast(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_people_vaccinated
FROM CovidPortfolioProject..CovidDeaths dea
JOIN CovidPortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
