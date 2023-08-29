
-- 1. Global Case Numbers
SELECT SUM(new_cases) as total_cases
     , SUM(cast(new_deaths as int)) as total_deaths
	 , SUM(cast(new_deaths as int))/SUM(new_cases)*100 as death_percentage
FROM CovidPortfolioProject..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1, 2


-- 2. COVID death numbers by Continents
SELECT location
	 , SUM(cast(new_deaths as int)) as total_death_count
FROM CovidPortfolioProject..CovidDeaths
WHERE continent IS NULL
  AND location NOT IN ('World', 'European Union', 'International')
GROUP BY location
ORDER BY total_death_count DESC

-- 3. Countries in order of highest percent of population infected with COVID
SELECT location
	 , population
	 , MAX(total_cases) as highest_infection_count
	 , MAX((total_cases/population))*100 as percent_population_infected
FROM CovidPortfolioProject..CovidDeaths
GROUP BY location
	   , population
ORDER BY percent_population_infected DESC

-- 4. Countries in order of highest percent of population infected with COVID, displayed by dates reported
SELECT location
	 , population
	 , date
	 , MAX(total_cases) as highest_infection_count
	 , MAX ((total_cases/population))*100 as percent_population_infected
FROM CovidPortfolioProject..CovidDeaths
GROUP BY location
	   , population
	   , date
ORDER BY percent_population_infected DESC