"""Tests for content brief schemas and keyword clustering (Phase B/C)."""

import pytest
from faceless_marketing.content import (
    Claim,
    ContentBrief,
    ContentStatus,
    ContentType,
    KeywordCluster,
    create_claim,
    create_content_brief,
    create_keyword_cluster,
)


class TestClaim:
    """Test Claim validation and serialization."""

    def test_valid_claim(self):
        claim = create_claim(
            text="Performance improved by 40%",
            evidence_source="benchmark_2024_q1.json",
            rule_id="BENCHMARK_001"
        )
        assert claim.text == "Performance improved by 40%"
        assert claim.evidence_source == "benchmark_2024_q1.json"
        assert claim.rule_id == "BENCHMARK_001"
        assert claim.unsupported is False

    def test_claim_with_unsupported_flag(self):
        claim = create_claim(
            text="This is the best library ever",
            evidence_source="manual_review",
            unsupported=True
        )
        assert claim.unsupported is True

    def test_rejects_empty_text(self):
        with pytest.raises(ValueError, match="claim text must be a non-empty string"):
            create_claim(text="", evidence_source="source")

    def test_rejects_empty_evidence_source(self):
        with pytest.raises(ValueError, match="evidence_source must be a non-empty string"):
            create_claim(text="Valid claim", evidence_source="")

    def test_rejects_control_characters_in_text(self):
        with pytest.raises(ValueError, match="claim text must not contain control characters"):
            create_claim(text="Claim\x00with\x01control", evidence_source="source")

    def test_rejects_control_characters_in_evidence(self):
        with pytest.raises(ValueError, match="evidence_source must not contain control characters"):
            create_claim(text="Valid claim", evidence_source="source\x00bad")

    def test_as_dict_serialization(self):
        claim = create_claim(
            text="New API endpoint added",
            evidence_source="changelog_v0.2.md",
            rule_id="CHANGELOG_001",
            unsupported=False
        )
        d = claim.as_dict()
        assert d == {
            "text": "New API endpoint added",
            "evidence_source": "changelog_v0.2.md",
            "rule_id": "CHANGELOG_001",
            "unsupported": False,
        }


class TestKeywordCluster:
    """Test KeywordCluster validation and serialization."""

    def test_valid_cluster(self):
        cluster = create_keyword_cluster(
            topic="performance optimization",
            keywords=["fast", "benchmark", "latency"],
            priority=8
        )
        assert cluster.topic == "performance optimization"
        assert cluster.keywords == ("fast", "benchmark", "latency")
        assert cluster.priority == 8

    def test_default_priority(self):
        cluster = create_keyword_cluster(
            topic="documentation",
            keywords=["guide", "tutorial"]
        )
        assert cluster.priority == 5

    def test_rejects_empty_topic(self):
        with pytest.raises(ValueError, match="topic must be a non-empty string"):
            create_keyword_cluster(topic="", keywords=["kw"])

    def test_rejects_empty_keywords(self):
        with pytest.raises(ValueError, match="keywords must be a non-empty tuple"):
            create_keyword_cluster(topic="test", keywords=[])

    def test_rejects_empty_keyword_item(self):
        with pytest.raises(ValueError, match="each keyword must be a non-empty string"):
            create_keyword_cluster(topic="test", keywords=["valid", ""])

    def test_rejects_control_characters_in_keywords(self):
        with pytest.raises(ValueError, match="keywords must not contain control characters"):
            create_keyword_cluster(topic="test", keywords=["bad\x00keyword"])

    def test_rejects_invalid_priority_low(self):
        with pytest.raises(ValueError, match="priority must be an integer between 1 and 10"):
            create_keyword_cluster(topic="test", keywords=["kw"], priority=0)

    def test_rejects_invalid_priority_high(self):
        with pytest.raises(ValueError, match="priority must be an integer between 1 and 10"):
            create_keyword_cluster(topic="test", keywords=["kw"], priority=11)

    def test_strips_whitespace(self):
        cluster = create_keyword_cluster(
            topic="  spaced topic  ",
            keywords=["  kw1  ", "kw2"]
        )
        assert cluster.topic == "spaced topic"
        assert cluster.keywords == ("kw1", "kw2")

    def test_as_dict_serialization(self):
        cluster = create_keyword_cluster(
            topic="security",
            keywords=["audit", "vulnerability", "patch"],
            priority=9
        )
        d = cluster.as_dict()
        assert d == {
            "topic": "security",
            "keywords": ["audit", "vulnerability", "patch"],
            "priority": 9,
        }


class TestContentBrief:
    """Test ContentBrief validation and serialization."""

    def test_minimal_valid_brief(self):
        claim = create_claim("Feature X released", "changelog.md")
        brief = create_content_brief(
            id="brief-001",
            content_type=ContentType.RELEASE_NOTE,
            title="Release v0.2.0",
            hypothesis="Users need to know about Feature X",
            claims=[claim],
            target_audience="developers",
            channel="github"
        )
        assert brief.id == "brief-001"
        assert brief.content_type == ContentType.RELEASE_NOTE
        assert brief.status == ContentStatus.DRAFT
        assert len(brief.claims) == 1
        assert brief.keyword_clusters == ()

    def test_full_brief_with_clusters(self):
        claim = create_claim("40% faster", "benchmark.json")
        cluster = create_keyword_cluster("performance", ["fast", "speed"], priority=7)
        brief = create_content_brief(
            id="brief-002",
            content_type=ContentType.TECHNICAL_ANNOUNCEMENT,
            title="Performance Breakthrough",
            hypothesis="Developers care about speed",
            claims=[claim],
            target_audience="backend engineers",
            channel="dev.to",
            status=ContentStatus.REVIEW,
            keyword_clusters=[cluster],
            metadata={"author": "team"}
        )
        assert brief.status == ContentStatus.REVIEW
        assert len(brief.keyword_clusters) == 1
        assert brief.metadata == {"author": "team"}

    def test_rejects_empty_id(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="id must be a non-empty string"):
            create_content_brief(
                id="",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_invalid_content_type(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="content_type must be a ContentType enum"):
            create_content_brief(
                id="b1",
                content_type="invalid",
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_empty_title(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="title must be a non-empty string"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_empty_hypothesis(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="hypothesis must be a non-empty string"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="",
                claims=[claim],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_no_claims(self):
        with pytest.raises(ValueError, match="at least one claim is required"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_invalid_claims_type(self):
        with pytest.raises(ValueError, match="all claims must be Claim instances"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=["not a claim"],
                target_audience="audience",
                channel="channel"
            )

    def test_rejects_empty_target_audience(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="target_audience must be a non-empty string"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="",
                channel="channel"
            )

    def test_rejects_empty_channel(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="channel must be a non-empty string"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel=""
            )

    def test_rejects_invalid_status(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="status must be a ContentStatus enum"):
            create_content_brief(
                id="b1",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel="channel",
                status="invalid"
            )

    def test_rejects_control_characters_in_fields(self):
        claim = create_claim("test", "source")
        with pytest.raises(ValueError, match="must not contain control characters"):
            create_content_brief(
                id="b\x001",
                content_type=ContentType.RELEASE_NOTE,
                title="Title",
                hypothesis="Hypothesis",
                claims=[claim],
                target_audience="audience",
                channel="channel"
            )

    def test_as_dict_serialization(self):
        claim = create_claim("Feature released", "changelog.md")
        cluster = create_keyword_cluster("release", ["new", "feature"])
        brief = create_content_brief(
            id="brief-003",
            content_type=ContentType.BLOG_POST,
            title="New Feature Blog",
            hypothesis="Blog posts drive engagement",
            claims=[claim],
            target_audience="users",
            channel="medium",
            status=ContentStatus.PUBLISHED,
            keyword_clusters=[cluster],
            metadata={"views": "1000"}
        )
        d = brief.as_dict()
        assert d["id"] == "brief-003"
        assert d["content_type"] == "blog_post"
        assert d["status"] == "published"
        assert len(d["claims"]) == 1
        assert len(d["keyword_clusters"]) == 1
        assert d["metadata"] == {"views": "1000"}

    def test_deterministic_output(self):
        """Verify that as_dict produces consistent output."""
        claim = create_claim("Test", "source")
        brief1 = create_content_brief(
            id="det-001",
            content_type=ContentType.RELEASE_NOTE,
            title="Deterministic Test",
            hypothesis="Testing determinism",
            claims=[claim],
            target_audience="devs",
            channel="github"
        )
        brief2 = create_content_brief(
            id="det-001",
            content_type=ContentType.RELEASE_NOTE,
            title="Deterministic Test",
            hypothesis="Testing determinism",
            claims=[claim],
            target_audience="devs",
            channel="github"
        )
        assert brief1.as_dict() == brief2.as_dict()


class TestContentTypeEnum:
    """Test ContentType enum values."""

    def test_all_content_types_exist(self):
        assert ContentType.RELEASE_NOTE.value == "release_note"
        assert ContentType.TECHNICAL_ANNOUNCEMENT.value == "technical_announcement"
        assert ContentType.DOCUMENTATION_UPDATE.value == "documentation_update"
        assert ContentType.BLOG_POST.value == "blog_post"
        assert ContentType.TUTORIAL.value == "tutorial"
        assert ContentType.CASE_STUDY.value == "case_study"


class TestContentStatusEnum:
    """Test ContentStatus enum values."""

    def test_all_statuses_exist(self):
        assert ContentStatus.DRAFT.value == "draft"
        assert ContentStatus.REVIEW.value == "review"
        assert ContentStatus.PUBLISHED.value == "published"
        assert ContentStatus.ARCHIVED.value == "archived"
