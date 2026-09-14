#!/usr/bin/env python3
"""One-shot migration of the 11 Jekyll posts into src/content/blog/.

Strips the leading `## Title` heading (title moves to frontmatter), derives
pubDate from the Jekyll filename, and writes curated descriptions/tags.
Kept in the repo for provenance; not needed after the migration.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '_posts'
DST = ROOT / 'src' / 'content' / 'blog'

POSTS = {
    '2022-10-03-Impediments-Scrum.md': dict(
        slug='impediments-scrum',
        title='Removing Impediments during Scrum in a Start-up',
        description='Common impediments a scrum master meets in a startup — communication breakdowns, resource constraints, shifting priorities — and practical ways to clear them.',
        tags=['agile', 'leadership'],
    ),
    '2022-10-26-RFID-for-Food-Industry.md': dict(
        slug='rfid-for-food-industry',
        title='RFID Technologies for FoodTech',
        description='A technical buyer’s guide to RFID in the food supply chain: frequencies, protocols, antennas and scanners, and how to choose between them.',
        tags=['engineering', 'supply-chain'],
    ),
    '2022-11-27-Servant-leader.md': dict(
        slug='servant-leader',
        title='Transforming Negativity into Growth',
        description='How a servant leader turns negative team members and situations into growth, with concrete tactics for building a culture of trust and respect.',
        tags=['leadership'],
    ),
    '2022-12-07-IT-values-mission-vision.md': dict(
        slug='it-values-mission-vision',
        title='The Crucial Role of Mission, Vision, and Values in Tech and IT Teams',
        description='Why a clear mission, vision and values give IT teams direction and better prioritisation — illustrated with a real team charter I helped shape.',
        tags=['leadership', 'strategy'],
    ),
    '2022-12-20-IT-risk-management.md': dict(
        slug='it-risk-management',
        title='A Comprehensive Guide to IT Risk Assessment for Startups and SMEs',
        description='IT and tech risk assessment, management and mitigation for startups and SMEs, using recognised frameworks like ITIL, ISO 27001 and NIST.',
        tags=['risk', 'strategy'],
    ),
    '2023-01-07-Digital-transformation-and-navigating-change.md': dict(
        slug='digital-transformation-and-navigating-change',
        title='Navigating Change Management in Digital Transformation',
        description='Change-management techniques for digital transformation, combining lessons from Viaene, Johnson and Kim with real-world cases.',
        tags=['transformation', 'leadership'],
    ),
    '2023-01-23-Technical-debt.md': dict(
        slug='technical-debt',
        title='Technical Debt — Balancing Speed, Agility, and Long-Term Success',
        description='The trade-offs behind technical debt: when it buys you speed, when it sinks you, and how experienced scrum masters and product owners keep it in check.',
        tags=['engineering', 'strategy'],
    ),
    '2023-02-15-Tech-Stack-Selection.md': dict(
        slug='tech-stack-selection',
        title='Navigating Tech Stack Decisions',
        description='How to choose a tech stack that fits your project’s requirements, team skills and long-term scalability — and the traps to avoid.',
        tags=['engineering', 'strategy'],
    ),
    '2023-02-28-Importance-Of-Cadence.md': dict(
        slug='importance-of-cadence',
        title='The Importance of Cadence in Agile Software Development',
        description='Why a steady delivery rhythm is the most underrated ingredient of agile: predictability, better planning, and healthier collaboration.',
        tags=['agile'],
    ),
    '2023-03-14-Data-Science-Skills.md': dict(
        slug='data-science-skills',
        title='Data Science: A Focus on Talent',
        description='Data science succeeds on talent, not tooling: the hiring challenges and the mix of skills that make a data scientist actually effective.',
        tags=['data-science', 'leadership'],
    ),
    '2023-03-23-Setting-up-data-science.md': dict(
        slug='setting-up-data-science',
        title='Setting up Data Science',
        description='Distributed vs capability-centric data science organisations: the risks, the trade-offs, and why centralised capability usually wins long-term.',
        tags=['data-science', 'strategy'],
    ),
}


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for fname, meta in POSTS.items():
        src = SRC / fname
        text = src.read_text(encoding='utf-8')
        # Drop the first `## Title` heading; frontmatter now carries the title.
        body = re.sub(r'^\s*##\s+.*?\n', '', text, count=1).lstrip('\n')
        pub = fname[:10]
        tags = ', '.join(f'"{t}"' for t in meta['tags'])
        desc = meta['description'].replace('"', '\\"')
        fm = (
            '---\n'
            f'title: "{meta["title"]}"\n'
            f'description: "{desc}"\n'
            f'pubDate: {pub}\n'
            f'tags: [{tags}]\n'
            'legacy: true\n'
            '---\n\n'
        )
        (DST / f'{meta["slug"]}.md').write_text(fm + body, encoding='utf-8')
        print(f'{fname} -> {meta["slug"]}.md')


if __name__ == '__main__':
    main()
